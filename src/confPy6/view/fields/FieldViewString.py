# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit

from confPy6.view.FieldView import FieldView


class FieldViewString(FieldView):
    value_changed = Signal(str)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self, view: QLineEdit = None) -> QLineEdit:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        # old
        if view is None:
            le = QtWidgets.QLineEdit(str(self.parent_field.value))
        else:
            le: QLineEdit = view
        le.setToolTip(f"({self.parent_field.field_name}) {self.parent_field._description}")
        self.ui_edit_fields.append(le)
        self.parent_field._module_logger.debug(f"Registering LineEdit {le}")
        self.ui_edit_fields[-1].textEdited.connect(lambda d: self._on_text_edited(le, d))

        # new
        return le

    def _on_text_edited(self, f, value):
        self.parent_field._module_logger.debug(f"LineEdit {f} changed to {value}.")
        self.parent_field.set(value)

    def _on_value_changed_partial(self, value):
        for edit in self.ui_edit_fields:
            edit.setText(value)
        # for tree_item in self.tree_items:
        #    tree_item.setText(1, value)
        # self.parent_field._set(value)
