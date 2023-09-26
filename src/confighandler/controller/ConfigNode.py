import datetime
import logging

import yaml

from src.confighandler.controller.CSignal import CSignal
from src.confighandler.controller.Field import Field
from src.confighandler.view.ConfigView import ConfigView


class ConfigNode(object):
    field_changed = CSignal()


    cur_time = datetime.datetime.now()



    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.logger = logging.getLogger(self.name)
        self.owner = None
        self._level = 0

        self.view = ConfigView(self)

        self.fields = {}
        self.configs = {}
        self.keywords =  {
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
        print(state)
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
        print(f"Deserializing {content}")
        for attr, val in content.items():
            # Check if the attribute is not of type GenericConfig
            # therefore get the attribute type of this class
            # print(f"Parsing {attr} with content: {val}")
            if attr == self.name:
                print(f"Found own config")
                self.deserialize(val)
            elif attr in self.__dict__:
                field = getattr(self, attr)
                if not isinstance(field, ConfigNode):
                    print(f"Deserializing field {attr} with content: {val}")
                    field.set(val)
                else:
                    print(f"Deserializing config {attr} with content: {val}")
                    getattr(self, attr).deserialize(val)

    # ==================================================================================================================
    # Registering the fields and configs
    # ==================================================================================================================
    def register(self):
        # print("register")
        self._register_field()
        self._register_config()

    def _register_field(self):
        for attr, val in self.__dict__.items():
            if isinstance(val, Field):
                #val.__set_name__(self.__class__.__name__, attr)
                self.fields[attr] = val
                #val.register(self.keywords, self.view.keywords_changed)
                val.register(self.__class__.__name__, attr,
                             self.keywords, self.field_changed)
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
    def save(self, file: str, background_save = True):
        # write the string to a file
        with open(file, 'w+') as stream:
            stream.write(self.serialize())
            #print(self.serialize())
        if not background_save:
            self.logger.debug(f"Saved config to {file}")
        # with open(file, 'w+') as stream:
        #    yaml.dump(self, stream) # Dump it as a xaml file
        # with open(file, 'w+') as stream:
        #    stream.write(
        # print(self._dump(cfg))

    def load(self, file: str):
        # load the yaml file
        with open(file, 'r') as stream:
            conent = yaml.load(stream, Loader=yaml.FullLoader)
        self.deserialize(conent)

    # ==================================================================================================================
    # Functions that happens on a change
    # ==================================================================================================================
    def _on_field_changed(self):
        # Emit that a field has changed, thus the keywords have changed
        #print(f"Field changed {self.keywords}")
        for attr, val in self.fields.items():
            val: Field
            val._on_keyword_changed()

        if self._level == 0:
            #print(f"Saving config {self.name}")
            self.save("config.yaml", background_save=True)