import confighandler as cfg


class LaserConfig(cfg.ConfigNode):

    def __init__(self, enable_log=False) -> None:
        super().__init__(enable_log=enable_log)
        self.wavelength_range = cfg.Field(850)
        self.velocity = cfg.Field(2.0)
        self.acceleration = cfg.Field(1.0)
        self.deceleration = cfg.Field(1.0)
        self.port = cfg.Field("USB 0")

        self.register()
