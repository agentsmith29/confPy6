import pathlib
from pathlib import Path
from confighandler.controller.Field import Field


class FieldPath(Field):
    # value_changed = Signal(str)

    def __init__(self, value: str, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        # self._value_replaced_keywords = self.replace_keywords(self.value)
        self.view = FieldViewPath(self)
        self._input = self.value
        # self.ui_btn_opens = []

    # ==================================================================================================================
    # Getter and Setter for value retrival
    # ==================================================================================================================
    def get(self) -> pathlib.Path:
        return Path(self.replace_keywords(str(self.value)))

    def _yaml_repr(self):
        return str('"@Path:<' + str(Path(self.value).as_posix()) + '>"')
