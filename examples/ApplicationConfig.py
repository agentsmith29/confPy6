import sys
from pathlib import Path

from src import confighandler as cfg
from examples.LaserConfig import LaserConfig


class ApplicationConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        self.output_directory: cfg.Field[Path] = cfg.Field(Path("C:\\{wafer_nr}"),
                                                           friendly_name="Output Directory",
                                                           description="The version of the wafer")

        self.wafer_version: cfg.Field[str] = cfg.Field("v1.0",
                                                       friendly_name="wafer_version",
                                                       description="The version of the wafer")

        self.wafer_number: cfg.Field[int] = cfg.Field(1,
                                                      friendly_name="wafer_number",
                                                      description="The version of the wafer")

        self.wafer_nr: cfg.Field[str] = cfg.Field("12345ABCD_{wafer_number}",
                                                  friendly_name="wafer_nr",
                                                  description="The version of the wafer")

        self.wafer_number2: cfg.Field[tuple] = cfg.Field((1, 2),
                                                         friendly_name="wafer_number2",
                                                         description="The version of the wafer")

        self.wafer_list: cfg.Field[list] = cfg.Field([1, 2],
                                                     friendly_name="wafer_list",
                                                     description="The version of the wafer")

        self.laser_config: LaserConfig = LaserConfig()


        self.register()
