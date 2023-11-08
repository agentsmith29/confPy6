# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewTuple import FieldViewTuple


class FieldTuple(Field):
    def __init__(self, value: tuple, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewTuple(self)

    def _yaml_repr(self):
        return str(self.value)

    #def _set(self, value):
    #    self._value = value
    #    self._on_value_changed(value)

    #def _on_value_changed(self, value):
    #    self.view.value_changed.emit(value)
