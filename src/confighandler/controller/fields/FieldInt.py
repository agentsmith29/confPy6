from src.confighandler.controller.Field import Field
from src.confighandler.view.fields.FieldViewInt import FieldViewInt


class FieldInt(Field):
    def __init__(self, value: int, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewInt(self)

    def _yaml_repr(self):
        return int(self.value)
