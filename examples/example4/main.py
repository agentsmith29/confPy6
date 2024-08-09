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
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget, QPushButton
from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    app = QApplication(sys.argv)


    # setup the logging module+
    logging.basicConfig(level=logging.DEBUG)

    config = ApplicationConfig()
    config.module_log_enabled = True
    config.module_log_level = logging.DEBUG

    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)
    grd.addWidget(config.view.widget(), 0, 0)
    # grd.addWidget(config.view.widget(), 1, 0)

    btn_config_editor = QPushButton()
    btn_config_editor.setText("Open Config Editor")
    btn_config_editor.clicked.connect(config.show_config_editor)
    grd.addWidget(btn_config_editor, 1, 0)

    window.setCentralWidget(wdg)
    # print(config.load('config.yaml'))

    window.show()

    sys.exit(app.exec())
