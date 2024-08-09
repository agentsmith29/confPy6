import logging
import sys
from pathlib import Path



sys.path.append('../../src/')

import confPy6 as cfg
from confPy6.controller.SelectableList import SelectableList


class BConfSub(cfg.ConfigNode):

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.sc_field_bool: cfg.Field[bool] = cfg.Field(False)

        self.sc_field_float: cfg.Field[float] = cfg.Field(29.1)

        self.sc_field_int: cfg.Field[int] = cfg.Field(5)

        self.sc_field_path: cfg.Field[Path] = cfg.Field(Path('../'))

        self.sc_field_sel_list: cfg.Field[SelectableList] = cfg.Field(
            SelectableList(
                [1, 2, 3],
                selected_index=2,
                description='ms'))
        self.sc_field_str: cfg.Field[str] = cfg.Field('testing')

        self.sc_field_tuple: cfg.Field[tuple] = cfg.Field((13, 5))

        self.register()
