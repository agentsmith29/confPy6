# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit, QSpinBox, QCheckBox

from confighandler.view.FieldView import FieldView


class FieldViewBool(FieldView):
    value_changed = Signal(bool)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self, view: QCheckBox = None) -> QCheckBox:
        """
        Returns a QLineEdit for the UI
        The UI is automatically updated when the value is changed.
        """
        if view is None:
            dsp = QCheckBox()
        else:
            dsp: QCheckBox = view
        dsp.setToolTip(f"({self.parent_field.name}) {self.parent_field._description}")
        dsp.setChecked(self.parent_field.value)
        self.ui_edit_fields.append(dsp)
        self.ui_edit_fields[-1].stateChanged.connect(self._on_state_changed)

        return self.ui_edit_fields[-1]

    def _on_state_changed(self, state):
        self.parent_field.set(bool(state))

    # def _on_keyword_changed(self, keywords):
    #    pass

    def _on_value_changed(self, value):
        # print(f">>> {self.parent_field.name}: Value changed {value}")
        for edit in self.ui_edit_fields:
            edit: QCheckBox  # Just for typehinting
            edit.setChecked(bool(value))
