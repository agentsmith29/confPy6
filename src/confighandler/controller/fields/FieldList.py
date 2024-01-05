# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewList import FieldViewList


class FieldList(Field):
    def __init__(self, value: tuple, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewList(self)
        self._allowed_types = (list, [tuple])

    def _yaml_repr(self):
        return str(self.value)
