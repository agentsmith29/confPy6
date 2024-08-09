import logging
import sys
from pathlib import Path

from tests.BConfSub import BConfSub

sys.path.append('../../src/')

import confPy6 as cfg
from confPy6.controller.SelectableList import SelectableList


class BConf_BConfSub(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        self.field_bool: cfg.Field[bool] = cfg.Field(True)

        self.field_float: cfg.Field[float] = cfg.Field(0.0)

        self.field_int: cfg.Field[int] = cfg.Field(0)

        self.field_path: cfg.Field[Path] = cfg.Field(Path('./'))

        self.field_sel_list: cfg.Field[SelectableList] = cfg.Field(
            SelectableList(
                [6, 7, 8],
                selected_index=0,
                description='ms'))
        self.field_str: cfg.Field[str] = cfg.Field('')

        self.field_tuple: cfg.Field[tuple] = cfg.Field((0, 0))

        self.sub_conf = BConfSub(parent=self)

        self.register()
