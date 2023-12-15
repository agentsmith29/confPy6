# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import confighandler as ch
from confighandler.controller.Field import T


class FieldSelectableList(ch.Field):
    def __init__(self, value: ch.SelectableList, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = ch.FieldViewSelectableList(self)

    def get_list(self) -> list:
        return list(self._value)

    @property
    def value(self):
        return self._value[self._value.selected_index]

    @property
    def _value_to_emit(self):
        return self._value.selected_index

    def _set(self, value):
        self._value.selected_index = value

    def _yaml_repr(self):
        return str(f"{self._value} -> {self.value}")
