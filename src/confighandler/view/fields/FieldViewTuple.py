from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLineEdit

from confighandler.view.FieldView import FieldView


class FieldViewTuple(FieldView):
    value_changed = Signal(tuple)

    def __init__(self, parent_field: 'FieldTuple'):
        super().__init__(parent_field)

    def ui_field(self, view: QLineEdit = None) -> QLineEdit:
        """

        """
        self.ui_edit_fields.append(QtWidgets.QLineEdit(
            str(self.parent_field.value)))
        self.ui_edit_fields[-1].textEdited.connect(self._on_text_edited)
        # self.ui_edit_fields[-1] : QtWidgets.QLineEdit
        self.ui_edit_fields[-1].editingFinished.connect(self._on_edited_finished)

        # new
        return self.ui_edit_fields[-1]

    def _on_text_edited(self, value):
        self.parent_field.set(value)

    def _on_value_changed(self, value):
        for edit in self.ui_edit_fields:
            edit.setText(str(value))

    def _input_validation(self, value):
        # First check if an ',' is present
        if isinstance(value, str) and "," in value:
            # Remove brackets if present
            tv = value.replace('(', '').replace(')', '').replace(' ', '')
            # Split by comma
            tv_split = tv.split(",")
            tup = []
            for t in tv_split:
                if t.isnumeric() and float(t).is_integer():
                    tup.append(int(t))
                elif t.isnumeric():
                    tup.append(float(t))
                else:
                    tup.append(t)
            return tuple(tup)
        elif isinstance(value, tuple):
            return value
        else:
            raise ValueError("Invalid input or unknown type (not str or tuple)")

    def _on_edited_finished(self):
        # print(f"edited finished: {self.parent_field.value} of type {type(self.parent_field.value)}")
        try:
            conv_value = self._input_validation(self.parent_field.value)
            # print(f"converted value: {conv_value} of type {type(conv_value)}")
            self.parent_field.set(conv_value)
            for edit in self.ui_edit_fields:
                edit: QLineEdit
                print(edit.styleSheet())
                edit.setStyleSheet(None)
        except Exception as e:
            self._display_error(e)
            self.parent_field.set(self.parent_field.value)
