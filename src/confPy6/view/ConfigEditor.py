from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QTreeWidget, QMainWindow

import confPy6


class ConfigEditor(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        #self.parent = parent

        wdg = QWidget()
        grd = QtWidgets.QVBoxLayout()
        wdg.setLayout(grd)
        #grd.addWidget(config.view.widget(max_level=1), 0, 0)
        # grd.addWidget(config.view.widget(), 1, 0)

        tree = QTreeWidget()
        tree.setHeaderLabels(confPy6.tree_view_header())
        tree.addTopLevelItem(config.ui_tree_widget_item(tree, max_level=1))
        tree.resizeColumnToContents(0)
        grd.addWidget(tree)

        keyword_widget = config.keyword_widget()
        grd.addWidget(keyword_widget)

        self.setCentralWidget(wdg)