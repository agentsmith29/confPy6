import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTreeWidget
from rich.logging import RichHandler

from ApplicationConfig import ApplicationConfig

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # setup the logging module
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="DEBUG", format=FORMAT, datefmt="[%X]", handlers=[
            RichHandler(rich_tracebacks=True)
        ]
    )

    config = ApplicationConfig(enable_log=True)
    print(config.load('./configs/ApplicationConfig.yaml'))
    config.autosave(enable=True, path='./configs_autosave')

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

    window.setCentralWidget(wdg)
    #print(config.save('config.yaml'))
    #print(config.load('config.yaml'))

    window.show()

    sys.exit(app.exec())
    # config.wafer_nr = "1234"

    # config.save("test.yaml")


