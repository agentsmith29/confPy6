import logging
import sys

from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QTreeView, QPushButton

from ConfigHandler.controller.VAutomatorConfig import VAutomatorConfig
from ConfigHandler.controller.GenericConfig import GenericConfig


class ConfigViewOld(QWidget):

    def __init__(self, vaut_config: VAutomatorConfig):
        super().__init__()

        # Load YAML file
        #with open(yaml_file_path, 'r') as f:
        self.data = vaut_config

        # Create controller and populate with YAML data
        self.model = QStandardItemModel()
        self._populate_model(self.model, self.data)

        # Create view and set controller
        self.view = QTreeView()
        self.view.setModel(self.model)
        self.view.expandAll()

        # Connect double-click signal to edit mode
        self.view.doubleClicked.connect(self._edit_mode)

        # Create textbox and button for value editing
        self.textbox = QLineEdit()
        self.button = QPushButton('Update')
        self.button.clicked.connect(self._update_value)

        # Create layout and add widgets
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.textbox)
        self.layout.addWidget(self.button)

        # Set widget layout
        self.setLayout(self.layout)

    def repopulate(self, data):

        self.data = data
        self.model = QStandardItemModel()
        self._populate_model(self.model, data)
        self.view.setModel(self.model)

    def _populate_model(self, parent, data):
        """
        Recursively populate QStandardItemModel with YAML data
        """
        if isinstance(data, dict):
            for key, value in data.items():
                item = QStandardItem(str(key))
                parent.appendRow(item)
                self._populate_model(item, value)
        if isinstance(data, GenericConfig):
            for key, value in data.__dict__.items():
                item = QStandardItem(str(key))
                parent.appendRow(item)
                self._populate_model(item, value)
        elif isinstance(data, list):
            for value in data:
                item = QStandardItem(str(value))
                parent.appendRow(item)
            #self._populate_model(item, str(data))
        elif isinstance(data, logging.Logger):
            pass
        else:
            item = QStandardItem(str(data))
            parent.appendRow(item)

    def _edit_mode(self, index):
        """
        Enter edit mode when double-clicked on item
        """
        self.view.edit(index)

    def _update_value(self):
        """
        Update YAML data and controller when button is clicked
        """
        # Get selected index
        index = self.view.currentIndex()

        # Get new value from textbox
        new_value = self.textbox.text()

        # Update YAML data
        self._update_data(self.data, index, new_value)

        # Update controller
        self.model.clear()
        self._populate_model(self.model, self.data)
        self.view.expandAll()

    def _update_data(self, data, index, new_value):
        """
        Recursively update YAML data
        """
        if index.column() == 0:
            # Update key
            key = index.selected_measurements()
            data[new_value] = data.pop(key)
        else:
            # Update value
            parent = index.parent().selected_measurements()
            if isinstance(data, dict):
                data[parent][index.row()] = new_value
            elif isinstance(data, list):
                data[parent][index.row()] = new_value
        # Recursively update child nodes
        for row in range(self.model.rowCount(index)):
            child_index = self.model.index(row, 0, index)
            self._update_data(data, child_index, new_value)



if __name__ == '__main__':
    # Initialize Qt application
    app = QApplication(sys.argv)

    vaut = VAutomatorConfig.load_config("./configs/init_config.yaml")

    # Create main window
    window = ConfigViewOld(vaut)
    window.show()

    # Run Qt event loop
    sys.exit(app.exec())

