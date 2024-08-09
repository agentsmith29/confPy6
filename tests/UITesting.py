import unittest

from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication

from tests.BConf import BConf

_instance = None

class UsesQApplication(unittest.TestCase):
    '''Helper class to provide QApplication instances'''

    qapplication = True

    def setUp(self):
        '''Creates the QApplication instance'''

        # Simple way of making instance a singleton
        super(UsesQApplication, self).setUp()
        global _instance
        if _instance is None:
            _instance = QApplication([])

        self.app = _instance

    def tearDown(self):
        '''Deletes the reference owned by self'''
        del self.app
        super(UsesQApplication, self).tearDown()



class TestUI_FieldIntView(UsesQApplication):

    def test_increment_decrement(self):
        config = BConf()
        config.field_int.set(23)
        # increment the QSpinBox
        QTest.keyClick(config.field_int.view.ui_field(), QtCore.Qt.Key.Key_Up)
        self.assertEqual(config.field_int.get(), 24)

        QTest.keyClick(config.field_int.view.ui_field(), QtCore.Qt.Key.Key_Down)
        self.assertEqual(config.field_int.get(), 23)

    def test_increment_decrement_with_variable(self):
        config = BConf()
        config.field_str.set("myvar_{BConf.field_int}")
        config.field_int.set(23)

        # Check if value is set to 23
        self.assertEqual(config.field_str.get(), "myvar_23")
        # increment the QSpinBox
        QTest.keyClick(config.field_int.view.ui_field(), QtCore.Qt.Key.Key_Up)
        self.assertEqual(config.field_str.get(), "myvar_24")
        # decrement the QSpinBox
        QTest.keyClick(config.field_int.view.ui_field(), QtCore.Qt.Key.Key_Down)
        self.assertEqual(config.field_str.get(), "myvar_23")

