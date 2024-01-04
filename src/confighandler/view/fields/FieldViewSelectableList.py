# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtCore
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QVBoxLayout, QLabel, QPushButton, QMenu

import confighandler as ch


class FieldViewAddEntry(QWidget):
    value_changed = Signal(tuple)

    def __init__(self):
        super().__init__()

        self.setWindowTitle('PySide Window')
        self.setGeometry(100, 100, 400, 200)

        self.init_ui()

    def init_ui(self):
        # Create layout
        layout = QVBoxLayout()

        # Create input fields
        self.value_label = QLabel('Value:')
        self.value_input = QLineEdit(self)

        self.desc_label = QLabel('Description:')
        self.desc_input = QLineEdit(self)

        # Create buttons
        ok_button = QPushButton('OK', self)
        abort_button = QPushButton('Abort', self)

        # Connect buttons to functions
        ok_button.clicked.connect(self.on_ok_clicked)
        abort_button.clicked.connect(self.on_abort_clicked)

        # Add widgets to layout
        layout.addWidget(self.value_label)
        layout.addWidget(self.value_input)
        layout.addWidget(self.desc_label)
        layout.addWidget(self.desc_input)
        layout.addWidget(ok_button)
        layout.addWidget(abort_button)

        # Set layout for the main window
        self.setLayout(layout)

    def on_ok_clicked(self):
        value = self.value_input.text()
        description = self.desc_input.text()
        print(f'OK Clicked - Value: {value}, Description: {description}')
        self.value_changed.emit((value, description))
        self.close()

    def on_abort_clicked(self):
        print('Abort Clicked')
        self.close()


class FieldViewSelectableList(ch.FieldView):
    value_changed = Signal(tuple)

    def __init__(self, parent_field: ch.FieldSelectableList):
        super().__init__(parent_field)
        self.add_entry = FieldViewAddEntry()
        self.add_entry.value_changed.connect(self._on_entry_added)

    def ui_field(self, view: QComboBox = None) -> QComboBox:
        """

        """
        # self.ui_edit_fields: list(QComboBox)
        if view is None:
            cb = QComboBox()
            # self.parent_field.logger.info(f"{self.parent_field}: *** NEW FieldViewSelectableList.ui_field {cb}"
        else:
            cb: QComboBox = view

        self.ui_edit_fields.append(cb)
        self._populate(cb)

        cb.setToolTip(f"({self.parent_field.name}) {self.parent_field._description}")
        cb.setCurrentIndex(self.parent_field.get_current_index())
        cb.currentIndexChanged.connect(self._on_index_changed)
        cb.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)  # Qt.CustomContextMenu
        cb.customContextMenuRequested.connect(
            lambda pos: self.show_context_menu(pos, field=cb))

        # self.ui_edit_fields[-1].editingFinished.connect(self._on_edited_finished)
        # new
        return cb

    def _populate(self, cb: QComboBox, reset=False):
       # for cb in self.ui_edit_fields:
        cb: QComboBox
        #cb.currentIndexChanged.connect(None)
        if reset:
            cb.clear()
        sel_list = self.parent_field.get_selectable_list()
        for v in sel_list:
            cb.addItem(f"{v[1]}", v[0])
        cb.addItem("<Add new ...>", self.add_entry.show)
        #cb.currentIndexChanged.connect(self._on_index_changed)


    def show_context_menu(self, pos, field):
        index = field.currentIndex()
        if index >= 0:
            context_menu = QMenu(field)
            delete_action = QAction('Delete', field)
            delete_action.triggered.connect(lambda: self.delete_item(field))
            context_menu.addAction(delete_action)

            action = context_menu.exec_(field.mapToGlobal(pos))

    def delete_item(self, field):
        index = field.currentIndex()
        if index >= 0:
            self.parent_field.get_selectable_list().remove(index)
        for cb in self.ui_edit_fields:
            cb: QComboBox
            self._populate(cb, True)

    def _on_index_changed(self, index: int, *args, **kwargs):
        data = self.ui_edit_fields[-1].itemData(index)
        if callable(data):
            data()
        else:
            self.parent_field.set(int(index))

    def _on_entry_added(self, tup):
        self.parent_field.get_selectable_list().append(tup[0], description=tup[1])
        for cb in self.ui_edit_fields:
            cb: QComboBox
            self._populate(cb, True)
        self.parent_field.set(len(self.parent_field.get_selectable_list()) - 1)
        self.parent_field.csig_field_changed.emit()

    def _on_value_changed_partial(self, value):
        for edit in self.ui_edit_fields:
            edit: QComboBox
            # self.parent_field.logger.info(f"{edit}: Setting index to {value}")
            edit.setCurrentIndex(value)
            edit.setToolTip(f"<{edit.currentData()}> ({self.parent_field.name}) {self.parent_field._description}")
