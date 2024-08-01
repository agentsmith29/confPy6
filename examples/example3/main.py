import logging
import sys
import time
import os

# Get the path to the current file
file_path, _ = os.path.split(os.path.realpath(__file__))
src_path = f"{file_path}/../../src"
print("src_path:", src_path)
sys.path.append(src_path)

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget
from ApplicationConfig import ApplicationConfig


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup the logging module+
    logging.basicConfig(level=logging.DEBUG)

    config = ApplicationConfig()
    config.module_log_enabled = True
    config.module_log_level = logging.DEBUG

    #config.load('./configs/ApplicationConfig.yaml')
    #config.autosave(enable=True, path='./')
    # print(config.wafer_version)
    # config.wafer_version.get()
    # config.wafer_number.get()
    # print(config.wafer_version)

    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)
    grd.addWidget(config.view.widget(), 0, 0)
    # grd.addWidget(config.view.widget(), 1, 0)

    tree = QTreeWidget()

    tree.setColumnCount(3)
    tree.setHeaderLabels(["Name", "Type", "asdf"])
    tree.addTopLevelItem(config.view.ui_tree_widget_item(tree))
    grd.addWidget(tree, 2, 0)

    btn_set = QtWidgets.QPushButton("Set Wafer Number to 5")
    btn_set.clicked.connect(lambda: config.wafer_number.set("5"))
    grd.addWidget(btn_set, 3, 0)

    btn_save = QtWidgets.QPushButton("Save Config")
    #btn_save.clicked.connect(lambda: config.save('./configs/ApplicationConfig.yaml'))
    grd.addWidget(btn_save, 4, 0)

    # Add a new combo box
    combo = QtWidgets.QComboBox()
    grd.addWidget(combo, 5, 0)
   # config.wafer_list1.view.add_new_view(combo)

   # config.wafer_list1.connect(test)

    window.setCentralWidget(wdg)
    # print(config.load('config.yaml'))

    window.show()

    sys.exit(app.exec())
    # config.wafer_nr = "1234"

    # config.save("test.yaml")
