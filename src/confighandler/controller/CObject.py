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


class CObject:

    def __init__(self, name: str = ""):
        if name is None or name == "":
            self.name = f"{self.__class__.__name__.replace('Field', '')}({hash(self)})"
        else:
            self.name = f"{name}({os.getpid()})"
        self._internal_logger, self._internal_log_handler = self.create_new_logger(f"(cfg) {self.name}")



    # ==================================================================================================================
    # Logging
    # ==================================================================================================================
    def create_new_logger(self, name: str) -> (logging.Logger, logging.Handler):
        qh = RichHandler(rich_tracebacks=True)
        _internal_logger = logging.getLogger(name)
        _internal_logger.handlers = [qh]
        _internal_logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(name)s %(message)s')
        qh.setFormatter(formatter)
        return _internal_logger, qh

    @property
    def internal_log_enabled(self):
        return not self._internal_logger.disabled

    @internal_log_enabled.setter
    def internal_log_enabled(self, enable: bool) -> None:
        """
        Enables or disables internal logging. If disabled, the internal logger will be disabled and no messages will be
        emitted to the state queue.
        :param enable: True to enable, False to disable
        """
        self._internal_logger.disabled = not enable

    @property
    def internal_log_level(self):
        return self._internal_logger.level

    @internal_log_level.setter
    def internal_log_level(self, level: int) -> None:
        """
        Sets the internal logging level.
        :param level:
        :return:
        """
        self._internal_logger.setLevel(level)