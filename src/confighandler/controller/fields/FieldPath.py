# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import pathlib
import re
from pathlib import Path

from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewPath import FieldViewPath


class FieldPath(Field):
    # value_changed = Signal(str)

    def __init__(self, value: str, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        # self._value_replaced_keywords = self.replace_keywords(self.value)
        self.view = FieldViewPath(self)
        self._input = self.value
        # self.ui_btn_opens = []

    # ==================================================================================================================
    # Getter and Setter for value retrival
    # ==================================================================================================================
    def get(self) -> pathlib.Path:
        return Path(self.replace_keywords(str(self.value)))

    def _yaml_repr(self):
        return str('"@Path:<' + str(Path(self.value).as_posix()) + '>"')

    def _field_parser(self, val):
        # Overwritten function, to replace the @Path keyword
        match = re.findall(r'@Path:<([^>]*)>', val)
        if len(match) > 0:
            self._internal_logger.info(f"Found @Path: {val}. Check syntax, multiple @Path: are not allowed in one field.")
            return {"value": Path(match[0])}
        elif len(match) == 0:
            self._internal_logger.debug(f"No @Path: found in {val}. Please check field.")
            return {"value": Path('./')}
    def __str__(self):
        return str(Path(self.value).as_posix())