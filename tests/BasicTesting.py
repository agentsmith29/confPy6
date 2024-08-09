import os
import pathlib
import unittest
import shutil
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

    @classmethod
    def tearDownClass(cls):
        pass
        #shutil.rmtree(TestCaseStoreConfigs.conf_tmp_folder)


class TestCaseOpenConfig(unittest.TestCase):
    assert_folder = './assert_configs/TestCaseOpenConfig'

    def test_open_config_1(self):
        config = BConf()
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
