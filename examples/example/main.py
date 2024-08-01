import logging
import sys
import os

# Get the path to the current file
file_path, _ = os.path.split(os.path.realpath(__file__))
src_path = f"{file_path}/../../src"
print("src_path:", src_path)
sys.path.append(src_path)

import time

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget
from ApplicationConfig import ApplicationConfig


if __name__ == "__main__":

    # setup the logging module+
    logging.basicConfig(level=logging.DEBUG)

    config = ApplicationConfig()
    config.module_log_enabled = True
    config.module_log_level = logging.DEBUG

    # config.save("test.yaml")
