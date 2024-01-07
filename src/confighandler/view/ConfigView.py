# -*- coding: utf-8 -*-
"""
Author(s): Christoph Schmidt <christoph.schmidt@tugraz.at>
Created: 2023-10-19 12:35
Package Version: 0.0.1
Description:
"""

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget, QLabel

import confighandler


class ConfigView(QObject):
    keywords_changed = Signal(dict)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.keywords = {}

    # ==================================================================================================================
    # UI handling
    # ==================================================================================================================
    def widget(self, max_level=1):
        self.parent._module_logger.debug("Creating widget for config view.")
        widget = QWidget()
        widget.setLayout(self._create_config_layout(max_level))
        return widget

    def ui_tree_widget_item(self, tree_widget, max_level=1):
        top_item = QtWidgets.QTreeWidgetItem()
        top_item.setText(0, f"{self.__class__.__name__}")

        for attr, val in self.parent.fields.items():
            item, le = val.view.ui_tree_widget_item()
            top_item.addChild(item)
            tree_widget.setItemWidget(item, 1, le)

        for attr, val in self.parent.configs.items():
            val: confighandler.ConfigNode
            if val.level <= max_level:
                top_item.addChild(val.view.ui_tree_widget_item(tree_widget))

        return top_item

    def _create_config_layout(self, max_level):
        """ Creates a pyside 6 layout based on the fields of the class."""
        grd_layout = QtWidgets.QGridLayout()
        row = 0
        # iterate through all class attributes
        for attr, val in self.parent.fields.items():
            grd_layout.addWidget(QLabel(val.friendly_name), row, 0)
            grd_layout.addWidget(val.view.ui_field(), row, 1)
            row += 1

        for attr, val in self.parent.configs.items():
            val: confighandler.ConfigNode
            if val.level <= max_level:
                gbox = QtWidgets.QGroupBox(val.name)
                gbox.setLayout(val.view._create_config_layout(max_level))
                grd_layout.addWidget(gbox, row, 0, 1, 2)
                row += 1

        return grd_layout