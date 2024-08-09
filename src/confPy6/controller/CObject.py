# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 
Description: 
"""
import logging
import os

from rich.logging import RichHandler

import confPy6


class CObject:

    def __init__(self, name: str = ""):

        if name is None or name == "":
            self.name = f"{self.__class__.__name__.replace('Field', '')}({hash(self)})"
        else:
            self.name = f"{name}({os.getpid()})"
        self._module_logger = self.create_new_logger(f"(cfg) {self.name}",
                                                     confPy6.global_module_log_enabled,
                                                     confPy6.global_module_log_level)

    # ==================================================================================================================
    # Logging
    # ==================================================================================================================
    def create_new_logger(self, name: str, enable: bool = True, level: int = 0,
                          propagate: bool = True) -> logging.Logger:
        _internal_logger = logging.getLogger(name)
        _internal_logger.handlers = [logging.NullHandler()]
        _internal_logger.setLevel(level)
        _internal_logger.disabled = not enable
        _internal_logger.propagate = propagate
        return _internal_logger

    @property
    def module_log_enabled(self):
        return not self._module_logger.disabled

    @module_log_enabled.setter
    def module_log_enabled(self, enable: bool) -> None:
        """
        Enables or disables internal logging. If disabled, the internal logger will be disabled and no messages will be
        emitted to the state queue.
        :param enable: True to enable, False to disable
        """
        if enable:
            self._module_logger.disabled = False
            CObject.global_module_log_enabled = False
            self._module_logger.debug(f"Logger {self._module_logger.name} enabled (Level {self._module_logger.level}).")
        else:
            self._module_logger.debug(f"Logger {self._module_logger.name} disabled.")
            CObject.global_module_log_enabled = True
            self._module_logger.disabled = True

    @property
    def module_log_level(self):
        return self._module_logger.level

    @module_log_level.setter
    def module_log_level(self, level: int) -> None:
        """
        Sets the internal logging level.
        :param level:
        :return:
        """
        self._module_logger.setLevel(level)
        if self._module_logger is not None:
            if level == logging.DEBUG:
                self._module_logger.debug(f"Module log level of {self.__class__.__name__} has been set to DEBUG.")
            elif level == logging.INFO:
                self._module_logger.debug(f"Module log level of {self.__class__.__name__} has been set to INFO.")
            elif level == logging.WARNING:
                self._module_logger.debug(f"Module log level of {self.__class__.__name__} has been set to WARNING.")
            elif level == logging.ERROR:
                self._module_logger.debug(f"Module log level of {self.__class__.__name__} has been set to ERROR.")
            elif level == logging.CRITICAL:
                self._module_logger.debug(f"Module log level of {self.__class__.__name__} has been set to CRITICAL.")
            else:
                self._module_logger.debug(
                    f"Module log level of {self.__class__.__name__} has been set to level {level}.")

        else:
            raise Exception("Can't set internal log level. Internal logger not initialized")
