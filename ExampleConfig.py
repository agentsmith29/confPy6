# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
Description: 
"""
import sys

sys.path.append("../src")
import confPy6 as cfg


class SecondConfig(cfg.ConfigNode):

    def __init__(self, internal_log=True) -> None:
        # Call the base class (important!)
        super().__init__(internal_log=internal_log)

        # Some fields
        # Create a field of type int. Set a default value, a friendly name and a description
        self.test_int: cfg.Field[int] = cfg.Field(1,
                                                  friendly_name="My Test Int",
                                                  description="This is just an integer")
        self.register()


class ApplicationConfig(cfg.ConfigNode):

    def __init__(self, internal_log=True) -> None:
        # Call the base class (important!)
        super().__init__(internal_log=internal_log)

        # Some fields
        # Create a field of type int. Set a default value, a friendly name and a description
        self.counter: cfg.Field[int] = cfg.Field(1,
                                                 friendly_name="My Counter",
                                                 description="This is just an integer")

        self.version: cfg.Field[str] = cfg.Field("v1.0",
                                                 friendly_name="Version",
                                                 description="The version")

        # You can also omit the friendly name and description
        self.check: cfg.Field[bool] = cfg.Field(False)

        # Some other fields
        # Also possible to create a field of type list
        self.my_tuple: cfg.Field[tuple] = cfg.Field((1, 2))
        self.any_list: cfg.Field[list] = cfg.Field([1, 2])

        # Even a nested config is possible
        self.second_config: SecondConfig = SecondConfig()

        # Don't forget to register the fields (important!)
        self.register()
