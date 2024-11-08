import logging
import sys
from pathlib import Path


sys.path.append('../../src/')

import confPy6 as cfg
from confPy6.controller.SelectableList import SelectableList
from LaserConfig import LaserConfig


class ApplicationConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()
        self.output_directory: cfg.Field[Path] = cfg.Field(Path("C:\\{LaserConfig.port}"))

        self.wafer_version: cfg.Field[str] = cfg.Field("v1.0",
                                                       friendly_name="wafer_version",
                                                       description="The version of the wafer")

        self.wafer_number: cfg.Field[float] = cfg.Field(12345.0,
                                                      friendly_name="wafer_number",
                                                      description="The version of the wafer",
                                                      range=(0, 150000))

        self.check: cfg.Field[bool] = cfg.Field(False, friendly_name="testcheck",
                                                      description="Testcheck")




        self.wafer_number2: cfg.Field[tuple] = cfg.Field((1, 2),
                                                         friendly_name="wafer_number2",
                                                         description="The version of the wafer")

        self.wafer_list: cfg.Field[list] = cfg.Field([1, 2],
                                                     friendly_name="wafer_list",
                                                     description="The version of the wafer")

        self.wafer_list1: cfg.Field[SelectableList] = cfg.Field(
            SelectableList([6, 7, 8],
            selected_index=0,
            description='ms'),
            friendly_name="wafer_list1",
            description="The version of the wafer")

        self.laser_config: LaserConfig = LaserConfig(self)

        self.register()
