# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewFloat import FieldViewFloat


class FieldFloat(Field):
    def __init__(self, value: float, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewFloat(self)

    def _yaml_repr(self):
        return float(self.value)
