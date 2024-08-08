# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import logging
import os
import re
from abc import abstractmethod
from pathlib import Path
from typing import Generic, T, TypeVar

from PySide6.QtWidgets import QApplication

import confPy6
from confPy6.controller.CObject import CObject
from confPy6.controller.CSignal import CSignal
#from confPy6.view.FieldView import FieldView


class FieldData(object):
    def __init__(self, name: str, value, friendly_name: str, description: str, env_var: str = None):
        self.name = name
        self._friendly_name = "Not Set or field not registered"
        self.value = [value, friendly_name, description]
        self.env_var = env_var


T = TypeVar('T')


class Field(Generic[T], CObject):
    changed = CSignal()

    def __init__(self, value: T, friendly_name: str = None, description: str = None,
                 env_var: str = None,
                 module_log=True, module_log_level=logging.WARNING):
        super().__init__(module_log, module_log_level)

        self.field_name = self.__class__.__name__
        self.logger = self.create_new_logger(self.name)

        self._data = FieldData(self.field_name, value, friendly_name, description, env_var)
        self._allowed_types = None
        self._friendly_name: str = friendly_name
        self._description: str = description
        self._value: T = value
        self._register_or_update_env_var()

        self.keywords = {}

        # The view, usd for handling the UI
        if QApplication.instance() is not None:
            self.view = self.create_view()
        else:
            self.view = None
        # Connected properties that should bet set if the field changes
        self.props = []

        self._module_logger.debug(f"Field {self.field_name} created with value {value} of type {type(value)}")

    def _register_or_update_env_var(self):
        if self._data.env_var is not None:
            os.environ[self._data.env_var] = self._env_converter()
        # delete the env var if the value is None
        elif self._data.env_var is None and self.get() is None:
            if self._data.env_var in os.environ.keys():
                del os.environ[self._data.env_var]

    def _env_converter(self):
        '''
            Converter to convert the type to the env variable
        '''
        return str(self.get())

    @abstractmethod
    def create_view(self):
        return confPy6.FieldView(self)

    def __new__(cls, value, friendly_name: str = None, description: str = None, env_var: str = None):
        # print(f"Field {cls.__name__} created with value {value} of type {type(value)} -> {isinstance(value, int)}")
        if isinstance(value, str):
            from confPy6.controller.fields.FieldString import FieldString
            return super().__new__(FieldString)
        elif type(value) is int:
            from confPy6.controller.fields.FieldInt import FieldInt
            return super().__new__(FieldInt)
        elif type(value) is float:
            from confPy6.controller.fields.FieldFloat import FieldFloat
            return super().__new__(FieldFloat)
        elif type(value) is bool:
            from confPy6.controller.fields.FieldBool import FieldBool
            return super().__new__(FieldBool)
        elif isinstance(value, Path):
            from confPy6.controller.fields.FieldPath import FieldPath
            return super().__new__(FieldPath)
        elif not isinstance(value, confPy6.SelectableList) and isinstance(value, tuple):
            from confPy6.controller.fields.FieldTuple import FieldTuple
            return super().__new__(FieldTuple)
        elif not isinstance(value, confPy6.SelectableList) and isinstance(value, list):
            from confPy6.controller.fields.FieldList import FieldList
            return super().__new__(FieldList)
        elif isinstance(value, confPy6.SelectableList):
            from confPy6.controller.fields.FieldSelectableList import FieldSelectableList
            return super().__new__(FieldSelectableList)

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        return f"{self.field_name}: {self._yaml_repr()} # {self.friendly_name}: {self.description}"

    def connect_property(self, instance, prop: property):
        self.props.append((instance, prop))

    def _set_all_props(self, value):
        # deactivate the set function since this can trigger an infinite loop
        bset = self.set
        self.set = lambda *args, **kwargs: None
        for inst, prop in self.props:
            prop.fset(inst, value)
        # Reactive the set function
        self.set = bset

    # ==================================================================================================================
    # Register the field to a configuration
    # ==================================================================================================================
    def register(self, owner, field_name, keywords, csig_field_changed: CSignal):
        """
        Register the keyword for the field. This is used for updating the keywords when the value is changed.
        Should only be called from a configuration class
        :param owner: The owner (parent) of the field
        :param field_name: The name of the field
        :param keywords: The keywords dict
        :param csig_field_changed: The signal that is emitted when the keywords are changed
        """

        self.field_name = field_name
        self.owner = owner
        if self._friendly_name is None:
            self._friendly_name = self.field_name

        # Assigns the global keywords dict to the field
        self.keywords = keywords
        # Assigns the csignal to the field, to notify the owner/parent about an value update
        self.csig_field_changed = csig_field_changed
        # self.keywords_changed = keyword_changed
        # self.keywords_changed.connect(self._on_keyword_changed)
        self.set_keywords()
        self._module_logger.info(f"Field '{self.field_name}' assigned to {self.owner}")
        self._module_logger.name = f"(cfg) {self.name}.{self.field_name}"

    # ==================================================================================================================
    # Set the keywords for the field
    # ==================================================================================================================
    def set_keywords(self):
        """Set the keywords for the field. Also updates the keywords dict if a value of a field is changed."""
        # self.keywords["{" + self.name + "}"] = self.value
        # self._internal_logger.info(f"Setting keywords for {self.name} to {self.value}")
        self.keywords[self.field_name] = str(self.value).replace(' ', '_').replace('.', '_').replace(',', '_')
        self.csig_field_changed.emit()

    def replace_keywords(self, fr: str):
        """Replaces the keywords in the given value with the values of the keywords dict"""
        # extract all occurencaes of strings between { and }

        if isinstance(fr, str):
            m = re.findall('{(.*?)}', fr)
            for kw in m:
                if kw in self.keywords.keys():
                    fr = fr.replace('{' + kw + '}', str(self.keywords[kw]))
                    if "{" in fr and "}" in fr:
                        fr = self.replace_keywords(fr)
            return fr
        else:
            return fr

    def _field_parser(self, val):
        # Dummy function, which can be overwritten, if the field should get parsed beforehand (e.g. when using pathes)
        return {"value": val}

    # ==================================================================================================================
    # Getter and Setter for value retrival
    # ==================================================================================================================
    @property
    def friendly_name(self):
        return self._friendly_name

    @property
    def description(self):
        return self._description

    @property
    def value(self) -> T:
        return self._value

    @property
    def _value_to_emit(self):
        """
        By default, the value will be emitted. Overwrite if you need another behavior
        :return:
        """

        return self._value

    def get(self) -> T:
        return self.replace_keywords(self.value)

    def check_type(self, value):
        type_allowed = False

        if isinstance(value, self._allowed_types[0]):
            return value

        if self._allowed_types is None:
            raise TypeError(f"No allowed types for {self.__class__.__name__}")

        if not isinstance(self._allowed_types, tuple) or len(self._allowed_types) < 2:
            raise TypeError(f"Allowed types not defined correctly for {self.__class__.__name__}")

        if self._allowed_types[1] is None:
            # If the list is None, no other types are allowed (e.g. strings)
            if isinstance(value, self._allowed_types[0]):
                print(f"Convert to first {self._allowed_types[0]}")
                type_allowed = True
        elif len(self._allowed_types[1]) == 0:
            # If the list is empty, all types are allowed (e.g. strings)
            type_allowed = True

        else:

            for t in self._allowed_types[1]:
                if isinstance(value, t):
                    type_allowed = True

        # No valid type has been found
        if not type_allowed:
            raise TypeError(
                f"Value for field {self.field_name} must be of type {self._allowed_types[0]}, not {type(value)}")
        else:
            # Valid type found, convert to first arg
            value = self._allowed_types[0](value)

        return value

    def set(self, value: T, *args, force_emit: bool = False, **kwargs):
        # typecheck
        # Check if allowed types are set
        value = self.check_type(value)
        if not self._value_to_emit == value or force_emit:
            self._module_logger.info(f"{self.field_name} = {value} ({type(value)})")
            self._set_all_props(value)
            self._set(value, *args, **kwargs)
            self.set_keywords()
            # self.view.value_changed.emit(self.value)
            # This emits a function that notifies the owner that the field has been set
            self.changed.emit(value)
            self.csig_field_changed.emit()

    def connect(self, func):
        self.changed.connect(func)

    # ==================================================================================================================
    # Things that should happen when the value is changed
    # ==================================================================================================================
    def _set(self, value, *args, **kwargs):
        self._value = value
        self._register_or_update_env_var()

    def _on_value_changed(self, value):
        raise NotImplementedError()

    def _on_keyword_changed(self):
        self.set(self._value_to_emit)
        if self.view is not None:
            self.view.value_changed.emit(self._value_to_emit)

    def _yaml_repr(self):
        raise NotImplementedError()

    def __str__(self):
        return self.get()

    def __repr__(self):
        return str(f"{self.__class__.__name__}")
