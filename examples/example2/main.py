import logging
import sys
import time
import os

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget
from rich import console
from rich.logging import RichHandler



# Get the path to the current file
file_path, _ = os.path.split(os.path.realpath(__file__))
src_path = f"{file_path}/../../src"
sys.path.append(src_path)
import confPy6
from ApplicationConfig import ApplicationConfig

class TestClass(QObject):
    signal = Signal(int)
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__} - fallback")
        super().__init__()
        self._wafer = 0

    @property
    def wafer(self):
        return self._wafer

    @wafer.setter
    def wafer(self, value):
        self._wafer = value
        self.logger.info(f"Wafer changed to {value}")
        self.signal.emit(value)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup the logging module
    FORMAT = "%(name)s %(message)s"
    logging.basicConfig(
        level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[logging.StreamHandler()]
    )

    confPy6.global_module_log_enabled = True
    confPy6.global_module_log_level = logging.INFO
    config = ApplicationConfig()

    config.autosave(enable=True, path='../configs_autosave/ApplicationConfig.yaml')

    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)
    grd.addWidget(config.view.widget(max_level=1), 0, 0)
    #grd.addWidget(config.view.widget(), 1, 0)

    tree = QTreeWidget()
    tree.setHeaderLabels(confPy6.tree_view_header())
    tree.addTopLevelItem(config.view.ui_tree_widget_item(tree, max_level=1))
    tree.resizeColumnToContents(0)
    grd.addWidget(tree, 1, 0)

    btn_set = QtWidgets.QPushButton("Set Wafer Number to 23.5")
    btn_set.clicked.connect(lambda: config.wafer_number.set(23.5))
    grd.addWidget(btn_set, 2, 0)

    btn_save = QtWidgets.QPushButton("Save Config")
    btn_save.clicked.connect(lambda: config.save('./configs/ApplicationConfig.yaml'))
    grd.addWidget(btn_save, 3, 0)

    # Add a new combo box
    combo = QtWidgets.QComboBox()
    grd.addWidget(combo, 5, 0)
    config.wafer_list1.view.add_new_view(combo)


   # config.wafer_list1.connect_property(testclass, TestClass.wafer)
    
    window.setCentralWidget(wdg)
    #print(config.load('config.yaml'))


    window.show()

    sys.exit(app.exec())
    # config.wafer_nr = "1234"

    # config.save("test.yaml")


