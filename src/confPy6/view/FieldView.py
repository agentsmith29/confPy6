# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""
from typing import TypeVar

from PySide6.QtCore import Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox, QStyle

import confPy6
#import confPy6.controller.Field as Field

from . import resources_rc
from ..controller.CObject import CObject


class FieldView(QWidget, CObject):
    value_changed = Signal(confPy6.T)

    def __init__(self, parent_field: confPy6.Field):
        super().__init__()
        CObject.__init__(self, f"{parent_field.owner}.{parent_field.field_name}.{self.__class__.__name__}")

        self.parent_field = parent_field

        self.label = None
        self.ui_edit_fields = []

        self.tree_items = []

        self.tree_view_item = QTreeWidgetItem(
            [
                self.parent_field.field_name,
                None,
                self.parent_field.description,
                self.parent_field.name,
                self.parent_field.get()
            ]
        )

        self.value_changed.connect(self._on_value_changed)

        if isinstance(confPy6.T, str):
            print(">>> String")

    def _on_value_changed(self, value):
        """
        Updates the UI when the value is changed.
        :param value:
        :return:
        """
        self.tree_view_item.setText(4, str(self.parent_field.get()))
        self._on_value_changed_partial(value)

    def _on_value_changed_partial(self, value):
        """
        Additional actions when the value is changed.
        :param value:
        :return:
        """
        raise NotImplementedError()

    def add_new_view(self, view: QWidget):
        self.ui_field(view)

    def ui_field(self, view: QWidget) -> QWidget:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        raise NotImplementedError()

    def ui_tree_widget_item(self):
        """Returns a QItem for the QTreeView"""
        item = self.ui_field()
        self.tree_view_item = QTreeWidgetItem([])
        #    [
        #        self.parent_field.field_name,
        #        None,
        #        self.parent_field.description,
        #        self.parent_field.name,
        #        self.parent_field.get()]
        #)
        # Update self.tree_view_item
        self.tree_view_item.setText(0, self.parent_field.field_name)
        self.tree_view_item.setText(2, self.parent_field.description)
        self.tree_view_item.setText(3, self.parent_field.name)
        self.tree_view_item.setText(4, str(self.parent_field.get()))
        # add icon
        if self.parent_field._data.env_var is not None:
            self.tree_view_item.setIcon(0, QIcon.fromTheme(QIcon.ThemeIcon.AudioVolumeLow))
        else:
            self.tree_view_item.setIcon(0, QIcon.fromTheme(QIcon.ThemeIcon.NetworkWired))

        # tree_view_item = QTreeWidgetItem([self.ui_field()])
        self.tree_items.append(self.tree_view_item)
        self.tree_view_item.setText(4, str(self.parent_field.get()))
        # tree_view_item.set
        return self.tree_items[-1], item

    def _input_validation(self, value):
        return value

    def _display_error(self, e: Exception):
        for edit in self.ui_edit_fields:
            edit.setStyleSheet("border: 1px solid red")

        self.parent_field.logger.error(e)
        # Display an error message
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setText("Error")
        self.msg.setInformativeText("Input is invalid")
        self.msg.setWindowTitle("Error")
        self.msg.show()
