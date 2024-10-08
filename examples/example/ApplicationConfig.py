import logging
import sys
from pathlib import Path
import confPy6 as cfg
from confPy6.controller.SelectableList import SelectableList
from LaserConfig import LaserConfig


class ApplicationConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        self.output_directory: cfg.Field[Path] = cfg.Field(Path("../../tests/t_{wafer_number}"))

        self.wafer_version: cfg.Field[str] = cfg.Field("v1.0",
                                                       friendly_name="wafer_version",
                                                       description="The version of the wafer")

        self.wafer_number: cfg.Field[int] = cfg.Field(1,
                                                      friendly_name="wafer_number",
                                                      description="The version of the wafer")

        self.check: cfg.Field[bool] = cfg.Field(False, friendly_name="testcheck",
                                                description="Testcheck")

        self.wafer_nr: cfg.Field[str] = cfg.Field("12345ABCD_{wafer_number}",
                                                  friendly_name="wafer_nr",
                                                  description="The version of the wafer")

        self.wafer_number2: cfg.Field[tuple] = cfg.Field((1, 2),
                                                         friendly_name="wafer_number2",
                                                         description="The version of the wafer")

        self.wafer_list: cfg.Field[list] = cfg.Field([1, 2],
                                                     friendly_name="wafer_list",
                                                     description="The version of the wafer")

        self.register()
