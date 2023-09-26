from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QWidget, QLabel


class ConfigView(QObject):
    keywords_changed = Signal(dict)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.keywords = {}

    # ==================================================================================================================
    # UI handling
    # ==================================================================================================================
    def widget(self):
        widget = QWidget()
        widget.setLayout(self._create_config_layout())
        return widget

    def ui_tree_widget_item(self, tree_widget):
        top_item = QtWidgets.QTreeWidgetItem()
        top_item.setText(0, self.__class__.__name__)

        for attr, val in self.parent.fields.items():
            item, le = val.view.ui_tree_widget_item()
            top_item.addChild(item)
            tree_widget.setItemWidget(item, 1, le)

        for attr, val in self.parent.configs.items():
            top_item.addChild(val.view.ui_tree_widget_item(tree_widget))
        return top_item

    def _create_config_layout(self):
        """ Creates a pyside 6 layout based on the fields of the class."""
        grd_layout = QtWidgets.QGridLayout()
        row = 0
        # iterate through all class attributes
        for attr, val in self.parent.fields.items():
            grd_layout.addWidget(QLabel(val.friendly_name), row, 0)
            grd_layout.addWidget(val.view.ui_field(), row, 1)
            row += 1

        for attr, val in self.parent.configs.items():
            # Add a group box
            gbox = QtWidgets.QGroupBox(val.name)
            gbox.setLayout(val.view._create_config_layout())
            grd_layout.addWidget(gbox, row, 0, 1, 2)
            row += 1

        return grd_layout