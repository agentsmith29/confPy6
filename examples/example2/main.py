import logging
import sys
import time

from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget
from rich.logging import RichHandler

from ApplicationConfig import ApplicationConfig

class TestClass:

    def _decorator(foo):
        def magic(self):
            print("start magic")
            foo(self)
            print("end magic")

        return magic
    def __init__(self, config: ApplicationConfig):
        self.config = config
        self._wafer = 0

    @property
    def wafer(self):
        return self._wafer

    @wafer.setter
    def wafer(self, value):
        self._wafer = value
        self.config.wafer_list1.set(value)
        print("Wafer changed to", value)
        #self.signal.emit(value)

def test(*args, **kwargs):
    print(f"test: {args}, {kwargs}")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup the logging module

    config = ApplicationConfig()
    testclass = TestClass(config)
    time.sleep(1)
    #config.autosave(enable=True, path='./configs_autosave')
    config.load('./configs/ApplicationConfig.yaml')
    config.autosave(enable=True, path='./')
    #print(config.wafer_version)
    #config.wafer_version.get()
    #config.wafer_number.get()
    #print(config.wafer_version)

    window = QMainWindow()
    wdg = QWidget()
    grd = QtWidgets.QGridLayout()
    wdg.setLayout(grd)
    grd.addWidget(config.view.widget(), 0, 0)
    #grd.addWidget(config.view.widget(), 1, 0)

    tree = QTreeWidget()


    tree.setColumnCount(3)
    tree.setHeaderLabels(["Name", "Type", "asdf"])
    tree.addTopLevelItem(config.view.ui_tree_widget_item(tree))
    grd.addWidget(tree, 2, 0)

    btn_set = QtWidgets.QPushButton("Set Wafer Number to 123")
    btn_set.clicked.connect(lambda: config.wafer_nr.set("123"))
    grd.addWidget(btn_set, 3, 0)

    btn_save = QtWidgets.QPushButton("Save Config")
    btn_save.clicked.connect(lambda: config.save('./configs/ApplicationConfig.yaml'))
    grd.addWidget(btn_save, 4, 0)

    # Add a new combo box
    combo = QtWidgets.QComboBox()
    grd.addWidget(combo, 5, 0)
    config.wafer_list1.view.add_new_view(combo)


    config.wafer_list1.connect(test)
    
    window.setCentralWidget(wdg)
    #print(config.load('config.yaml'))


    window.show()

    sys.exit(app.exec())
    # config.wafer_nr = "1234"

    # config.save("test.yaml")

