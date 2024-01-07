# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

import datetime
import logging
import os
import pathlib

import yaml

from .CObject import CObject
from .CSignal import CSignal
from .Field import Field
from ..view.ConfigView import ConfigView


class ConfigNode(CObject):
    field_changed = CSignal()

    cur_time = datetime.datetime.now()

    def __init__(self, module_log=True, module_log_level=logging.WARNING):
        super().__init__(module_log, module_log_level)

        self._autosave = False
        self.name = self.__class__.__name__
        self.config_file: pathlib.Path = pathlib.Path(f"./{self.name}.yaml")


        self.logger = self.create_new_logger(self.name)

        self.owner = None
        self._level = 0

        self.view = ConfigView(self)

        self.fields = {}
        self.configs = {}
        self.keywords = {
            "date": self.cur_time.strftime("%Y_%m_%d"),
            "time": self.cur_time.strftime("%H_%M"),
            "date_time": self.cur_time.strftime("%Y%m%d_%H%M")
        }

        self.field_changed.connect(self._on_field_changed)

    # ==================================================================================================================
    #
    # ==================================================================================================================
    def __set_name__(self, owner, name):
        self.name = name
        self.owner = owner

        # def __getstate__(self):
        """Used for serializing instances"""

        # start with a copy so we don't accidentally modify the object state
        # or cause other conflicts
        state = self.__dict__.copy()
        #print(state)
        # remove the unpicklable entries
        # del state['keywords_changed']

        return state

    # ==================================================================================================================
    # Serialization  and deserializing of the config
    # ==================================================================================================================
    def _serialize_sep(self, state):
        l = ""
        l1 = " "
        sep = "  "
        for i in range(self._level - 1):  l += sep
        for i in range(self._level): l1 += sep
        return l, l1

    def serialize(self) -> str:
        l, l1 = self._serialize_sep(self._level)
        if self._level == 0:
            dump = f"# - Configuration file stored {datetime.datetime.now()} - \n"
            dump += f"{self.name}: #!!python/object:controller.{self.__class__.__name__}\n"
        else:
            dump = f"{l}{self.name}: #!!python/object:controller.{self.__class__.__name__}\n"

        # Store the fields
        for attr, val in self.fields.items():
            dump += f"{l1}{val.serialize()}\n"

        # Store the configs
        if len(self.configs.items()) > 0:
            dump += f"\n# Sub-Configurations\n"
            for attr, val in self.configs.items():
                dump += f"{l1}{val.serialize()}\n"
        return dump

    def deserialize(self, content):
        """Deserializes the content of the config based on the yaml file"""
        self._module_logger.info(f"Deserializing {content}")
        for attr, val in content.items():
            # Check if the attribute is not of type GenericConfig
            # therefore get the attribute type of this class
            # print(f"Parsing {attr} with content: {val}")
            if attr == self.name:
                self.deserialize(val)
            elif attr in self.__dict__:
                if not isinstance(getattr(self, attr), ConfigNode):
                    self._module_logger.info(f"Deserializing field {attr} with content: {val}")
                    val = getattr(self, attr)._field_parser(val)
                    getattr(self, attr).set(**val, force_emit=True)
                else:
                    self._module_logger.info(f"Deserializing config {attr} with content: {val}")
                    getattr(self, attr).deserialize(val)

    @property
    def module_log_level(self):
        return self._module_logger.level

    @module_log_level.setter
    def module_log_level(self, level: int) -> None:
        self._module_logger.setLevel(level)
        for attr, val in self.__dict__.items():
            if isinstance(val, Field):
                self.fields[attr] = val
                val.module_log_level = self.module_log_level
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
            self._module_logger.debug(
                f"Logger {self._module_logger.name} enabled (Level {self._module_logger.level}).")
        else:
            self._module_logger.debug(f"Logger {self._module_logger.name} disabled.")
            self._module_logger.disabled = True

        for attr, val in self.__dict__.items():
            if isinstance(val, Field):
                self.fields[attr] = val
                val.module_log_enabled = self.module_log_enabled

    @property
    def level(self):
        return self._level

    # ==================================================================================================================
    # Registering the fields and configs
    # ==================================================================================================================
    def register(self):
        self._register_field()
        self._register_config()

    def _register_field(self):
        for attr, val in self.__dict__.items():
            if isinstance(val, Field):
                # val.__set_name__(self.__class__.__name__, attr)
                self.fields[attr] = val
                # val.register(self.keywords, self.view.keywords_changed)
                val.register(self.__class__.__name__, attr, self.keywords, self.field_changed)
                val.module_log_enabled = self.module_log_enabled
                val.module_log_level = self.module_log_level
        self.view.keywords_changed.emit(self.keywords)

    def _register_config(self):
        for attr, val in self.__dict__.items():
            if isinstance(val, ConfigNode):
                self.configs[attr] = val
                val.__set_name__(self.__class__.__name__, attr)
                val._level = self._level + 1
                # val.register_keyword(self.keywords, self.keywords_changed)
        # self.keywords_changed.emit(self.keywords)

    # ==================================================================================================================
    # I/O Operations
    # ==================================================================================================================
    def save(self, file: str=None, background_save=True):
        if file is not None:
            self.config_file = pathlib.Path(file)
        # write the string to a file
        with open(self.config_file, 'w+') as stream:
            stream.write(self.serialize())

        if not background_save:
            self._module_logger.debug(f"Saved config to {file}")


    def autosave(self, enable: bool = False, path: str = None):
        self._autosave = enable
        if self._autosave:
            if path is not None:
                # Check if the given path is a file or folder
                _path = pathlib.Path(f"./{path}")
                if _path.suffix == "" or path[-1].strip() == "/":
                    self.config_file = pathlib.Path(_path) / f"{self.name}.yaml"
                else:
                    self.config_file = pathlib.Path(_path)
                self.config_file.parent.mkdir(parents=True, exist_ok=True)

                self._module_logger.info(
                    f"Autosave enabled. File will be saved to  {self.config_file.absolute().as_posix()}")
                # Check if the path exists otherwise create it


    def load(self, file: str, as_auto_save: bool = False):
        # load the yaml file
        _file = pathlib.Path(file)
        self._module_logger.info(f"Loading config from {_file}")
        with open(str(_file.absolute().as_posix()), 'r') as stream:
            content = yaml.load(stream, Loader=yaml.FullLoader)
        self.deserialize(content)

        if as_auto_save:
            self._module_logger.debug(f"Configuration will be saved to {file}")
            self.config_file = pathlib.Path(file)

    # ==================================================================================================================
    # Functions that happens on a change
    # ==================================================================================================================
    def _on_field_changed(self, *args, **kwargs):
        # Emit that a field has changed, thus the keywords have changed
        for attr, val in self.fields.items():
            val: Field
            val._on_keyword_changed()
        if self._level == 0 and self._autosave:

            # Saves on every field change
            self.save(file=str(self.config_file.as_posix()), background_save=True)
            #self._module_logger.debug(f"Autosave to {self.config_file.absolute().as_posix()}")


