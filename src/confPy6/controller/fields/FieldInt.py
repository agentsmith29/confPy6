# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confPy6.controller.Field import Field
from confPy6.view.fields.FieldViewInt import FieldViewInt


class FieldInt(Field):
    def __init__(self, value: int, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self._allowed_types = (int, None)

    def create_view(self):
        return FieldViewInt(self)

    def _yaml_repr(self):
        return int(self.value)

    def __int__(self):
        # return str(self.as_dataframe())
        return int(self.get())