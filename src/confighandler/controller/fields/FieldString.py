from src.confighandler.controller.Field import Field
from src.confighandler.view.fields.FieldViewString import FieldViewString


class FieldString(Field):
    def __init__(self, value, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self._value_replaced_keywords = self.replace_keywords(self.value)
        self.view = FieldViewString(self)

    def _yaml_repr(self):
        return f"\"{self.value}\""
