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
        self._allowed_types = (Path, [pathlib.PurePosixPath, pathlib.PurePath,
                                      pathlib.PureWindowsPath,
                                      str])
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
            self._module_logger.info(f"Found @Path: {val}. Check syntax, multiple @Path: are not allowed in one field.")
            return {"value": Path(match[0])}
        elif len(match) == 0:
            self._module_logger.debug(f"No @Path: found in {val}. Please check field.")
            return {"value": Path('./')}

    def create_folder(self):
        print(f"Creating folder {self.get()}")
        # Check if path exists
        if not Path(self.get()).exists():
            Path(self.get()).mkdir(parents=True, exist_ok=True)
        # Check if path is now exists
        if Path(self.get()).exists():
            self._module_logger.info(f"Folder {self.get()} created.")
        else:
            self._module_logger.error(f"Folder {self.get()} could not be created.")
        self.csig_field_changed.emit()

    def __str__(self):
        return str(Path(self.value).as_posix())
