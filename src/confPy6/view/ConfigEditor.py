from PySide6 import QtWidgets
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QTreeWidget, QMainWindow, QMenu

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

        self.create_menu_bar()

        self.setCentralWidget(wdg)

    def create_menu_bar(self):
        # Create the menu bar
        menu_bar = self.menuBar()

        # Create file menu
        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)

        # Add actions to the file menu
        save_action = QAction("&Save", self)
        #save_action.triggered.connect(self.show_save_file_dialog)
        file_menu.addAction(save_action)
        save_action.triggered.connect(lambda: self.config.parent.save(use_open_file_dialog=True))

        self.enable_autosave_action = QAction("&Enable Autosave", self)
        # Checkable
        self.enable_autosave_action.setCheckable(True)
        self.enable_autosave_action.setChecked(self.config.parent.autosave_enable)
        self.enable_autosave_action.triggered.connect(self._enable_autosave)
        file_menu.addAction( self.enable_autosave_action)

        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create help menu
        help_menu = QMenu("&Help", self)
        menu_bar.addMenu(help_menu)

        # Add an about action to the help menu
        about_action = QAction("&About", self)
        #about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)

    def _enable_autosave(self):
        if self.enable_autosave_action:
            self.config.parent.autosave(True)
        else:
            self.config.parent.autosave(False)