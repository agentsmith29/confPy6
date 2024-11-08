# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QSpinBox

#from PySide6.QtWidgets import QSpinBox

from confPy6.view.FieldView import FieldView


class FieldViewInt(FieldView):
    value_changed = Signal(int)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self, view: QSpinBox = None) -> QSpinBox:
        """
        Returns a QLineEdit for the UI
        The UI is automatically updated when the value is changed.
        """
        if view is None:
            dsp = QtWidgets.QSpinBox()
        else:
            dsp: QSpinBox = view
        dsp.setToolTip(f"({self.parent_field.field_name}) {self.parent_field._description}")
        dsp.setRange(-100000, 100000)
        dsp.setValue(self.parent_field.value)
        self.ui_edit_fields.append(dsp)
        self.ui_edit_fields[-1].valueChanged.connect(self._on_value_edited)

        return self.ui_edit_fields[-1]

     def set_range(self, min, max):
        for uif in  self.ui_edit_fields:
            uif.setRange(min, max)
            uif.setValue(self.parent_field.value)
            
    def _on_value_edited(self, value):
        self.parent_field.set(int(value))

    # def _on_keyword_changed(self, keywords):
    #    pass

    def _on_value_changed_partial(self, value):

        for edit in self.ui_edit_fields:
            edit.setValue(int(value))
