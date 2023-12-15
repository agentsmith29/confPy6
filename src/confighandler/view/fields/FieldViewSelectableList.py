# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox

import confighandler as ch


class FieldViewSelectableList(ch.FieldView):

    value_changed = Signal(tuple)

    def __init__(self, parent_field: ch.FieldSelectableList):
        super().__init__(parent_field)

    def ui_field(self, view: QComboBox = None) -> QComboBox:
        """

        """
        #self.ui_edit_fields: list(QComboBox)
        if view is None:
            cb = QComboBox()
            self.parent_field.logger.info(f"{self.parent_field}: *** NEW FieldViewSelectableList.ui_field {cb}")

        else:
            cb: QComboBox = view

        for v in self.parent_field.get_list():
            cb.addItem(str(v))

        cb.setToolTip(f"({self.parent_field.name}) {self.parent_field._description}")
        self.ui_edit_fields.append(cb)
        self.ui_edit_fields[-1].setCurrentIndex(self.parent_field.get_current_index())
        self.ui_edit_fields[-1].currentIndexChanged.connect(self._on_index_changed)
        #self.ui_edit_fields[-1].editingFinished.connect(self._on_edited_finished)
        # new
        return self.ui_edit_fields[-1]

    def _on_index_changed(self, value):
        self.parent_field.set(int(value))

    def _on_value_changed(self, value):
        self.parent_field.logger.info(f"{self.parent_field}: FieldViewSelectableList._on_value_changed {value}"
                                      f"-> len {len(self.ui_edit_fields)}")
        for edit in self.ui_edit_fields:
            edit: QComboBox
            self.parent_field.logger.info(f"{edit}: Setting index to {value}")

            edit.setCurrentIndex(value)

