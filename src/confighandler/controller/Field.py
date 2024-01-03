# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import logging
import re
from pathlib import Path
from typing import Generic, T, TypeVar

from PySide6.QtCore import Signal

import confighandler
from confighandler.controller.CObject import CObject
from confighandler.controller.CSignal import CSignal
from confighandler.view.FieldView import FieldView


class FieldData(object):
    def __init__(self, name: str, value, friendly_name: str, description: str):
        self.name = name
        self.value = [value, friendly_name, description]


T = TypeVar('T')


class Field(Generic[T], CObject):

    changed = CSignal()
    def __init__(self, value: T, friendly_name: str = None, description: str = None,
                 internal_log=True, internal_log_level=logging.INFO):
        super().__init__()
        self.internal_log_enabled = internal_log
        self.internal_log_level = internal_log_level

        self.logger, self.log_handler = self.create_new_logger(self.name)

        self._data = FieldData(self.name, value, friendly_name, description)

        self._friendly_name: str = friendly_name
        self._description: str = description
        self._value: T = value

        self.keywords = {}

        # The view, usd for handling the UI
        self.view = FieldView(self)

        # Connected properties that should bet set if the field changes
        self.props = []

        self._internal_logger.debug(f"Field {self.__class__.__name__} created with value {value} of type {type(value)}")

    def __new__(cls, value, friendly_name: str = None, description: str = None):
        # print(f"Field {cls.__name__} created with value {value} of type {type(value)} -> {isinstance(value, int)}")
        if isinstance(value, str):
            from confighandler.controller.fields.FieldString import FieldString
            return super().__new__(FieldString)
        elif type(value) is int:
            from confighandler.controller.fields.FieldInt import FieldInt
            return super().__new__(FieldInt)
        elif type(value) is float:
            from confighandler.controller.fields.FieldFloat import FieldFloat
            return super().__new__(FieldFloat)
        elif type(value) is bool:
            from confighandler.controller.fields.FieldBool import FieldBool
            return super().__new__(FieldBool)
        elif isinstance(value, Path):
            from confighandler.controller.fields.FieldPath import FieldPath
            return super().__new__(FieldPath)
        elif not isinstance(value, confighandler.SelectableList) and isinstance(value, tuple):
            from confighandler.controller.fields.FieldTuple import FieldTuple
            return super().__new__(FieldTuple)
        elif not isinstance(value, confighandler.SelectableList) and isinstance(value, list):
            from confighandler.controller.fields.FieldList import FieldList
            return super().__new__(FieldList)
        elif isinstance(value, confighandler.SelectableList):
            from confighandler.controller.fields.FieldSelectableList import FieldSelectableList
            return super().__new__(FieldSelectableList)

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        return f"{self.name}: {self._yaml_repr()} # {self.friendly_name}: {self.description}"

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
    def register(self, owner, name, keywords, csig_field_changed: CSignal):
        """
        Register the keyword for the field. This is used for updating the keywords when the value is changed.
        Should only be called from a configuration class
        :param owner: The owner (parent) of the field
        :param name: The name of the field
        :param keywords: The keywords dict
        :param csig_field_changed: The signal that is emitted when the keywords are changed
        """

        self.name = name
        self.owner = owner
        formatter = logging.Formatter(f'%(name)s [{self.name}] %(message)s')

        self._internal_log_handler.setFormatter(formatter)
        if self._friendly_name is None:
            self._friendly_name = self.name

        # Assigns the global keywords dict to the field
        self.keywords = keywords
        # Assigns the csignal to the field, to notify the owner/parent about an value update
        self.csig_field_changed = csig_field_changed
        # self.keywords_changed = keyword_changed
        # self.keywords_changed.connect(self._on_keyword_changed)
        self.set_keywords()
        self._internal_logger.info(f"Field '{self.name}' assigned to {self.owner}")

    # ==================================================================================================================
    # Set the keywords for the field
    # ==================================================================================================================
    def set_keywords(self):
        """Set the keywords for the field. Also updates the keywords dict if a value of a field is changed."""
        # self.keywords["{" + self.name + "}"] = self.value
        # self._internal_logger.info(f"Setting keywords for {self.name} to {self.value}")
        self.keywords[self.name] = str(self.value).replace(' ', '_').replace('.', '_').replace(',', '_')
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

    def set(self, value: T, *args, force_emit: bool = False, **kwargs):
        if not self._value_to_emit == value or force_emit:
            self._internal_logger.info(f"{self.name} = {value} ({type(value)})")
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

    def _on_value_changed(self, value):
        raise NotImplementedError()

    def _on_keyword_changed(self):
        self.set(self._value_to_emit)
        self.view.value_changed.emit(self._value_to_emit)

    def _yaml_repr(self):
        raise NotImplementedError()

    def __str__(self):
        return self.get()

    def __repr__(self):
        return str(f"{self.__class__.__name__}")
