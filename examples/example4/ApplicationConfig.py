import logging
import pathlib
import sys
from pathlib import Path
import confPy6 as cfg

class ApplicationConfig(cfg.ConfigNode):

    def __init__(self) -> None:
        super().__init__()

        self.wafer_list: cfg.Field[Path] = cfg.Field(pathlib.Path('./'), env_var="WAFER_LIST")

        self.wafer_list2: cfg.Field[int] = cfg.Field(2)

        self.register()
