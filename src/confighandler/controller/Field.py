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

from confighandler.controller.CSignal import CSignal
from confighandler.view.FieldView import FieldView




class FieldData(object):
    def __init__(self, name: str, value, friendly_name: str, description: str):
        self.name = name
        self.value = [value, friendly_name, description]


T = TypeVar('T')


class Field(Generic[T]):

    def __init__(self, value: T, friendly_name: str = None, description: str = None):
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._data = FieldData(self.__class__.__name__, value, friendly_name, description)

        self._friendly_name: str = friendly_name
        self._description: str = description
        self._value: T = value

        self.keywords = {}

        # The view, usd for handling the UI
        self.view = FieldView(self)
        self.logger.debug(f"Field {self.__class__.__name__} created with value {value} of type {type(value)}")

    def __new__(cls, value, friendly_name: str = None, description: str = None):
        # <print(f"Field {cls.__name__} created with value {value} of type {type(value)}")
        if isinstance(value, str):
            from confighandler.controller.fields.FieldString import FieldString
            return super().__new__(FieldString)
        elif isinstance(value, int):
            from confighandler.controller.fields.FieldInt import FieldInt
            return super().__new__(FieldInt)
        elif isinstance(value, float):
            from confighandler.controller.fields.FieldFloat import FieldFloat
            return super().__new__(FieldFloat)
        elif isinstance(value, Path):
            from confighandler.controller.fields.FieldPath import FieldPath
            return super().__new__(FieldPath)
        elif isinstance(value, tuple):
            from confighandler.controller.fields.FieldTuple import FieldTuple
            return super().__new__(FieldTuple)
        elif isinstance(value, list):
            from confighandler.controller.fields.FieldList import FieldList
            return super().__new__(FieldList)

    def serialize(self):
        """Used for serializing instances. Returns the current field as a yaml-line."""
        return f"{self.name}: {self._yaml_repr()} # {self.friendly_name}: {self.description}"

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
        if self._friendly_name is None:
            self._friendly_name = self.name

        # Assigns the global keywords dict to the field
        self.keywords = keywords
        # Assigns the csignal to the field, to notify the owner/parent about an value update
        self.csig_field_changed = csig_field_changed
        # self.keywords_changed = keyword_changed
        # self.keywords_changed.connect(self._on_keyword_changed)
        self.set_keywords()
        self.logger.info(f"Field assigned to {self.owner} with name {self.name}")

    # ==================================================================================================================
    # Set the keywords for the field
    # ==================================================================================================================
    def set_keywords(self):
        """Set the keywords for the field. Also updates the keywords dict if a value of a field is changed."""
        # self.keywords["{" + self.name + "}"] = self.value
        #self.logger.info(f"Setting keywords for {self.name} to {self.value}")
        self.keywords[self.name] = str(self.value).replace(' ', '_').replace('.', '_').replace(',', '_')
        self.csig_field_changed.emit()


    def replace_keywords(self, fr: str):
        """Replaces the keywords in the given value with the values of the keywords dict"""
        # extract all occurencaes of strings between { and }

        if isinstance(fr, str):
            m = re.findall('\{(.*?)\}', fr)
            for kw in m:
                if kw in self.keywords.keys():
                    fr = fr.replace('{' + kw + '}', str(self.keywords[kw]))
                    if "{" in fr and "}" in fr:
                        fr = self.replace_keywords(fr)
            return fr
        else:
            return fr

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

    def get(self) -> T:
        return self.replace_keywords(self.value)

    def set(self, value: T):
        if not self.value == value:
            self.logger.info(f"{self.name} = {value} ({type(value)})")
            self._set(value)
            self.set_keywords()
            #self.view.value_changed.emit(self.value)
            # This emits a function that notifies the owner that the field has been set
            self.csig_field_changed.emit()

    # ==================================================================================================================
    # Things that should happen when the value is changed
    # ==================================================================================================================
    def _set(self, value):
        self._value = value

    def _on_value_changed(self, value):
        raise NotImplementedError()

    def _on_keyword_changed(self):
        self.set(self.value)
        #print(f"Field {self.__class__.__name__}._on_keyword_changed called: {self.value}: {str(self.value)}")
        self.view.value_changed.emit(self.value)

    def _yaml_repr(self):
        raise NotImplementedError()

    def __str__(self):
        return self.get()

    def __repr__(self):
        return str(f"{self.__class__.__name__}({self.value})")


