import confighandler as cfg


class LaserConfig(cfg.ConfigNode):

    def __init__(self, internal_log, internal_log_level) -> None:
        super().__init__(internal_log=internal_log, internal_log_level=internal_log_level)
        self.wavelength_range = cfg.Field(850)
        self.velocity = cfg.Field(2.0)
        self.acceleration = cfg.Field(1.0)
        self.deceleration = cfg.Field(1.0)
        self.port = cfg.Field("USB 0")

        self.register()
