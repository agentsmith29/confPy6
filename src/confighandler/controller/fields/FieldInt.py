# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewInt import FieldViewInt


class FieldInt(Field):
    def __init__(self, value: int, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewInt(self)
        self._allowed_types = [int, None]

    def _yaml_repr(self):
        return int(self.value)
