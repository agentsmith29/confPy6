# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""
import os
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QGridLayout, QFileDialog, QLineEdit

from confPy6.view.FieldView import FieldView


class FieldViewPath(FieldView):
    value_changed = Signal(str)

    def __init__(self, parent_field: 'FieldPath'):
        super().__init__(parent_field)
        self.ui_edit_fields_lbl = []
        self.ui_edit_fields_wdg = []
        self.ui_btn_opens = []
        self.ui_btn_creates = []

    def ui_field(self, view: QLineEdit = None) -> QWidget:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        wdg = QtWidgets.QWidget()
        grd = QGridLayout()
        grd.setContentsMargins(0, 0, 0, 0)

        if view is None:
            le = QLineEdit(str(self.parent_field.value), parent=self)
        else:
            le: QLineEdit = view

        if not Path(self.parent_field.get()).exists():
            le.setStyleSheet("border: 1px solid red")
        else:
            le.setStyleSheet("border: 1px solid green")

        #self.parent_field.set(self.parent_field.value)
        le.setToolTip(f"({self.parent_field.field_name}) {self.parent_field._description}\n"
                      f"Value: {self.parent_field.value}")
        self.ui_edit_fields_lbl.append(QtWidgets.QLabel(str(self.parent_field.get()), parent=self))
        self.ui_edit_fields.append(le)

        self.ui_edit_fields[-1].textEdited.connect(self._on_text_edited)
        self.ui_edit_fields[-1].editingFinished.connect(lambda: self._on_text_edited_finished(le.text()))

        btn_open = QtWidgets.QPushButton("...")
        self.ui_btn_opens.append(btn_open)
        self.ui_btn_opens[-1].clicked.connect(
            lambda: self._on_btn_clicked(self.ui_btn_opens[-1]))

        btn_create = QtWidgets.QPushButton("+")
        self.ui_btn_creates.append(btn_create)
        self.ui_btn_creates[-1].clicked.connect(
            lambda: self._on_btn_create_clicked(self))

        grd.addWidget(self.ui_edit_fields[-1], 0, 0)
        grd.addWidget(btn_open, 0, 1)
        grd.addWidget(btn_create, 0, 2)
        grd.addWidget(self.ui_edit_fields_lbl[-1], 1, 0, 1, 2)

        self.parent_field._module_logger.info(f"Registered QEditField for {self.ui_edit_fields[-1]}")

        wdg.setLayout(grd)
        self.ui_edit_fields_wdg.append(wdg)
        return self.ui_edit_fields_wdg[-1]

    def find_mount_point(self, path):
        path = os.path.abspath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
        return path

    def _on_btn_clicked(self, parent: QWidget):
        # create a file dialog to select a folder
        self.dlg = QFileDialog()
        self.dlg.setFileMode(QFileDialog.Directory)
        f = self.dlg.getExistingDirectory(parent)
        # Abort if nothing is selected
        if f == "":
            return

        path = Path(f)
        print(path)
        if self.find_mount_point(path) != self.find_mount_point(Path.cwd()):
            self.parent_field.set(str(path.absolute().as_posix()))
        else:
            rel_path = os.path.relpath(path.absolute().as_posix(), Path.cwd())
            flen = len(rel_path.split('..'))
            print(flen)
            if flen > 3:
                self.parent_field.set(str(path.absolute().as_posix()))
            else:
                self.parent_field.set(str(
                    Path(rel_path).as_posix()
                )
                )

    def _on_btn_create_clicked(self, p: QWidget):
        self.parent_field.create_folder()

    def _on_text_edited(self, value):
        #self.parent_field.set(value)
        pass

    def _on_text_edited_finished(self, value):
        print(f"Editing finished: Changed to {value}")
        self.parent_field.set(value)

    def _on_value_changed_partial(self, value: Path):
        # print(value)
        # Check if path exists
        for edit, lbl, btn_open in zip(self.ui_edit_fields, self.ui_edit_fields_lbl, self.ui_btn_creates):
            if not Path(self.parent_field.get()).exists():
                edit.setStyleSheet("border: 1px solid red")
                btn_open.setEnabled(True)
            else:
                edit.setStyleSheet("border: 1px solid green")
                btn_open.setEnabled(False)
            edit.setText(
                str(self.parent_field.value)
            )
            lbl.setText(
                str(self.parent_field.get())
            )
            # Update the QTreeWidgetItem in the TreeView



        # self.parent_field.set(value)
        # for tree_item in self.tree_items:
        #    tree_item.setText(1, value)
