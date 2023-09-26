from src.confighandler.controller.Field import Field
from src.confighandler.view.fields.FieldViewFloat import FieldViewFloat


class FieldFloat(Field):
    def __init__(self, value: float, friendly_name: str = None, description: str = None):
        super().__init__(value, friendly_name, description)
        self.view = FieldViewFloat(self)

    def _yaml_repr(self):
        return float(self.value)
