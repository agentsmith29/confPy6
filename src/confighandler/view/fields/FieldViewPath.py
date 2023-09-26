from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QFileDialog

from confighandler.view.FieldView import FieldView


class FieldViewPath(FieldView):
    value_changed = Signal(str)

    def __init__(self, parent_field: 'FieldPath'):
        super().__init__(parent_field)
        self.ui_edit_fields_lbl = []
        self.ui_edit_fields_wdg = []
        self.ui_btn_opens = []

    def ui_field(self) -> QWidget:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        wdg = QtWidgets.QWidget()
        grd = QGridLayout()
        grd.setContentsMargins(0, 0, 0, 0)

        self.ui_edit_fields_lbl.append(
            QtWidgets.QLabel(str(self.parent_field.get()), parent=self)
        )

        self.ui_edit_fields.append(
            QtWidgets.QLineEdit(str(self.parent_field.value), parent=self)
        )

        self.ui_edit_fields[-1].textEdited.connect(self._on_text_edited)

        btn_open = QtWidgets.QPushButton("...")
        self.ui_btn_opens.append(btn_open)
        self.ui_btn_opens[-1].clicked.connect(
            lambda: self._on_btn_clicked(self.ui_btn_opens[-1]))

        grd.addWidget(self.ui_edit_fields[-1], 0, 0)
        grd.addWidget(btn_open, 0, 1)
        grd.addWidget(self.ui_edit_fields_lbl[-1], 1, 0, 1, 2)

        self.parent_field.logger.info(f"Registered QEditField for {self.ui_edit_fields[-1]}")
        self.value_changed.connect(self._on_value_changed)

        wdg.setLayout(grd)
        self.ui_edit_fields_wdg.append(wdg)
        return self.ui_edit_fields_wdg[-1]

    def _on_btn_clicked(self, parent: QWidget):
        # create a file dialog to select a folder
        self.dlg = QFileDialog()
        self.dlg.setFileMode(QFileDialog.Directory)
        f = self.dlg.getExistingDirectory(parent)
        self.parent_field.set(str(Path(f).absolute()))
        # print(f)

    def _on_text_edited(self, value):
        self.parent_field.set(value)

    def _on_value_changed(self, value: Path):
        # print(value)
        # Check if path exists
        for edit, lbl in zip(self.ui_edit_fields, self.ui_edit_fields_lbl):
            if not Path(value).exists():
                edit.setStyleSheet("border: 1px solid red")
            else:
                edit.setStyleSheet("border: 1px solid green")
            edit.setText(
                str(self.parent_field.value)
            )
            lbl.setText(
                str(self.parent_field.get())
            )
        # self.parent_field.set(value)
        # for tree_item in self.tree_items:
        #    tree_item.setText(1, value)
