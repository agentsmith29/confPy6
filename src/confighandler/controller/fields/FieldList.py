from confighandler.controller.Field import Field
from confighandler.view.fields.FieldViewList import FieldViewList


class FieldList(Field):
    def __init__(self, value: tuple, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewList(self)

    def _yaml_repr(self):
        return str(self.value)
