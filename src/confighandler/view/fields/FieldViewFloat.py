from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit

from confighandler.view.FieldView import FieldView


class FieldViewFloat(FieldView):
    value_changed = Signal(float)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self) -> QLineEdit:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        dsp = QtWidgets.QDoubleSpinBox()
        dsp.setRange(-100000, 100000)
        dsp.setValue(self.parent_field.value)

        dsp.setDecimals(3)
        self.ui_edit_fields.append(dsp)
        self.value_changed.connect(self._on_value_changed)
        self.ui_edit_fields[-1].valueChanged.connect(self._on_value_edited)

        return self.ui_edit_fields[-1]

    def _on_value_edited(self, value):
        self.parent_field.set(float(value))

    # def _on_keyword_changed(self, keywords):
    #    pass

    def _on_value_changed(self, value):
        #print(f">>> {self.parent_field.name}: Value changed {value}")
        for edit in self.ui_edit_fields:
            edit.setValue(float(value))
