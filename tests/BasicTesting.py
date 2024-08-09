import logging
import os
import pathlib
import unittest
import shutil

from rich.logging import RichHandler

from tests.BConf import BConf
from tests.BConf_BConfSub import BConf_BConfSub


class TestCaseStoreConfigs(unittest.TestCase):
    conf_tmp_folder = './.unittests/TestCaseStoreConfigs'
    assert_folder = f'./assert_configs/TestCaseStoreConfigs'

    def test_store_folder_not_exists(self):

        base_conf = BConf()
        base_conf.save(f'{TestCaseStoreConfigs.conf_tmp_folder}/test_store_folder_not_exists.yaml')

        # Check if the file exists using os
        self.assertTrue(os.path.exists(f'{TestCaseStoreConfigs.conf_tmp_folder}/test_store_folder_not_exists.yaml'))

        # if test is passed, remove the non-empty folder
        #os.remove(f'{TestCaseStoreConfigs.conf_folder}/TC_test_store_BConf_1.yaml')

    def yaml_file_comp(self, original_path: str, saved_path: str):
        original = []
        saved = []
        # Compare the saved file with the original file
        with open(original_path, 'r') as f:
            for line in f.readlines():
                original.append(line)

        with open(saved_path, 'r') as f:
            for line in f.readlines():
                saved.append(line)

        self.assertEqual(len(original), len(saved))

        # First line contains timestamp. so ignore this
        for o, s in zip(original[1:], saved[1:]):
            self.assertEqual(o, s)

    def test_store_BConf_1(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_1.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_1.yaml'

        base_conf.save(saved_path)

        # Check if file has been saved
        self.assertTrue(os.path.exists(saved_path))

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_2(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_2.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_2.yaml'

        base_conf.field_bool.set(False)
        base_conf.field_float.set(12.3523)
        base_conf.field_int.set(2)
        base_conf.field_path.set(pathlib.Path('./testfolder123'))
        base_conf.field_sel_list.set(1)
        base_conf.field_str.set("myString")
        base_conf.field_tuple.set((-4, 2))

        base_conf.save(saved_path)

        # Check if file has been saved
        self.assertTrue(os.path.exists(saved_path))

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_BConfSub_1(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf_BConfSub()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_BConfSub_1.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_BConfSub_1.yaml'

        base_conf.save(saved_path)

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_BConfSub_2(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf_BConfSub()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_BConfSub_2.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_BConfSub_2.yaml'

        base_conf.field_bool.set(True)
        base_conf.field_float.set(52.6721)
        base_conf.field_int.set(55)
        base_conf.field_path.set(pathlib.Path('./testfolder_123'))
        base_conf.field_sel_list.set(0)
        base_conf.field_str.set("myString2")
        base_conf.field_tuple.set((-999999, 1))
        base_conf.save(saved_path)

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_BConfSub_3(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf_BConfSub()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_BConfSub_3.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_BConfSub_3.yaml'

        base_conf.field_int.set(34)
        base_conf.field_path.set(pathlib.Path('./testfolder_{BConf_BConfSub.field_int}'))
        self.assertEqual(base_conf.field_path.get().as_posix(), 'testfolder_34')

        base_conf.field_float.set(39.434)
        base_conf.field_str.set('myString{BConf_BConfSub.field_float}')
        self.assertEqual(base_conf.field_str.get(), 'myString39_434')

        base_conf.save(saved_path)

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_BConfSub_4(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf_BConfSub()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_BConfSub_4.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_BConfSub_4.yaml'

        base_conf.sub_conf.sc_field_float.set(29.1)
        base_conf.field_path.set(pathlib.Path('./testfolder_{BConfSub.sc_field_float}'))
        a = base_conf.field_path.get()
        self.assertEqual(a.as_posix(), 'testfolder_29_1')

        #base_conf.field_float.set(39.434)
        #base_conf.field_str.set('myString{BConf_BConfSub.field_float}')
        #self.assertEqual(base_conf.field_str.get(), 'myString39_434')

        base_conf.save(saved_path)

        self.yaml_file_comp(original_path, saved_path)

    def test_store_BConf_BConfSub_5(self):
        '''
        Store a config with a sub config
        '''
        base_conf = BConf_BConfSub()

        # Test against File: TC_OpenConfig_test_open_config_2.yaml
        original_path = f'{TestCaseStoreConfigs.assert_folder}/TC_test_store_BConf_BConfSub_5.yaml'
        saved_path = f'./{TestCaseStoreConfigs.conf_tmp_folder}/test_store_BConf_BConfSub_5.yaml'

        base_conf.sub_conf.sc_field_float.set(123)
        base_conf.sub_conf.sc_field_str.set("testing_{BConfSub.sc_field_float}")
        base_conf.field_str.set("myString_{BConfSub.sc_field_str}")
        self.assertEqual(base_conf.field_str.get(), "myString_testing_123_0")

        base_conf.save(saved_path)

        self.yaml_file_comp(original_path, saved_path)


    @classmethod
    def tearDownClass(cls):
        pass
        #shutil.rmtree(TestCaseStoreConfigs.conf_tmp_folder)


class TestCaseOpenConfig(unittest.TestCase):
    conf_tmp_folder = './.unittests/TestCaseOpenConfig'
    assert_folder = f'./assert_configs/TestCaseOpenConfig'


    @classmethod
    def setUpClass(cls):
        FORMAT = "%(name)s %(message)s"
        logging.basicConfig(
            level=logging.DEBUG, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )


    def test_open_config_1(self):

        config = BConf()
        #config.module_log_enabled = True
        #config.module_log_level = logging.DEBUG
        #print("Until here?")
        config.load(f'{TestCaseOpenConfig.assert_folder}/TC_OpenConfig_test_open_config_1.yaml')
        self.assertEqual(config.field_bool.get(), True)
        self.assertEqual(config.field_float.get(), 10.457)
        self.assertEqual(config.field_int.get(), 2)
        self.assertEqual(str(config.field_path.get().as_posix()), 'testcase1/folder')
        #self.assertEqual(config.field_sel_list.get(), 2)
        self.assertEqual(config.field_str.get(), 'test123')
        self.assertEqual(config.field_tuple.get(), (1, 5))

    def test_open_config_2(self):
        ''' Test open config with var substition'''
        config = BConf()
        config.load(f'{TestCaseOpenConfig.assert_folder}/TC_OpenConfig_test_open_config_2.yaml')
        self.assertEqual(config.field_bool.get(), True)
        self.assertEqual(config.field_float.get(), 10.457)
        self.assertEqual(config.field_int.get(), 2)
        self.assertEqual(str(config.field_path.get().as_posix()), 'testcase1/folder_2')
        # self.assertEqual(config.field_sel_list.get(), 2)
        self.assertEqual(config.field_str.get(), 'test_1__5_')
        self.assertEqual(config.field_tuple.get(), (1, 5))

    def test_open_config_wrong_int_type_1(self):
        config = BConf()
        # test if type error is thrown
        with self.assertRaises(TypeError):
            config.load(f'{TestCaseOpenConfig.assert_folder}/TC_test_open_config_wrong_int_type_1.yaml')


if __name__ == '__main__':
    unittest.main()
