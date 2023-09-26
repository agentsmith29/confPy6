from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QLineEdit

from confighandler.view.FieldView import FieldView


class FieldViewString(FieldView):
    value_changed = Signal(str)

    def __init__(self, parent_field):
        super().__init__(parent_field)

    def ui_field(self) -> QLineEdit:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        # old
        le = QtWidgets.QLineEdit(str(self.parent_field.value))
        self.ui_edit_fields.append(le)
        self.parent_field.logger.debug(f"Registering LineEdit {le}")
        self.ui_edit_fields[-1].textEdited.connect(lambda d: self._on_text_edited(le, d))
        self.value_changed.connect(self._on_value_changed)
        # new
        return le

    def _on_text_edited(self, f, value):
        self.parent_field.logger.debug(f"LineEdit {f} changed to {value}.")
        self.parent_field.set(value)

    def _on_value_changed(self, value):
        for edit in self.ui_edit_fields:
            edit.setText(value)
        # for tree_item in self.tree_items:
        #    tree_item.setText(1, value)
        # self.parent_field._set(value)
