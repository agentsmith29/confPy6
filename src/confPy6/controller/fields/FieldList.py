# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confPy6.controller.Field import Field
from confPy6.view.fields.FieldViewList import FieldViewList


class FieldList(Field):
    def __init__(self, value: tuple, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)

        self._allowed_types = (list, [tuple])

    def create_view(self):
        return FieldViewList(self)

    def _yaml_repr(self):
        return str(self.value)

    def __iter__(self):
        # return str(self.as_dataframe())
        return list(self.get())