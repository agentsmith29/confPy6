import logging
import sys
sys.path.append('../../src')
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
