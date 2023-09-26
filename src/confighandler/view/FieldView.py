from typing import T

from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QMessageBox


class FieldView(QWidget):
    value_changed = NotImplementedError()

    def __init__(self, parent_field):
        super().__init__()
        self.parent_field = parent_field

        self.label = None
        self.ui_edit_fields = []
        self.tree_items = []

        if isinstance(T, str):
            print(">>> String")

    def ui_field(self) -> QWidget:
        """
        Returns a QLineEdit for the UI.
        The UI is automatically updated when the value is changed.
        """
        raise NotImplementedError()

    def ui_tree_widget_item(self):
        """Returns a QItem for the QTreeView"""
        item = self.ui_field()
        tree_view_item = QTreeWidgetItem([self.parent_field.name, None, self.parent_field.description])
        # tree_view_item = QTreeWidgetItem([self.ui_field()])
        self.tree_items.append(tree_view_item)
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


