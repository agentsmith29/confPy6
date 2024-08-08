import logging

import confPy6 as cfg


class LaserConfig(cfg.ConfigNode):

    def __init__(self, parent: cfg.ConfigNode) -> None:
        super().__init__(True, logging.DEBUG, parent)
        self.wafer_nr: cfg.Field[str] = cfg.Field("12345ABCD_{wafer_number}",
                                                  friendly_name="wafer_nr",
                                                  description="The version of the wafer")

        self.wavelength_range = cfg.Field(850)
        self.velocity = cfg.Field(2.0)
        self.acceleration = cfg.Field(1.0)
        self.deceleration = cfg.Field(1.0)
        self.port = cfg.Field("USB 0")

        self.register()
