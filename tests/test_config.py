#!/usr/bin/env python

from unittest import TestCase, main, mock
from mc_srv_manager.config import Config
from pathlib import PosixPath


class testConfig(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testShouldRaiseValueErrorWhenNoSystemServiceUnitNameDefined(self) -> None:
        config = Config()
        try:
            service_unit_name = config.get_system_service_unit_name()
        except ValueError:
            # The exception was raised as expected
            pass
        else:
            # If we get here, then the ValueError was not raised
            # raise an exception so that the test fails
            raise AssertionError("ValueError was not raised")

    # def testCfgPathShouldBePosixPath(self) -> None:
    #     config = Config()
    #     self.assertIsInstance(
    #         config.get_cfg_file_path(),
    #         PosixPath
    #     )

    # def testServerPathShouldBeStrAndReturn(self) -> None:
    #     config = Config()
    #     expected_value = '/somewhere/is/server-path'
    #     with mock.patch.dict(config.config, {'env': {'server_path': expected_value}}):
    #         self.assertEqual(config.get_server_path(), expected_value)
    #         self.assertIsInstance(
    #             config.get_server_path(),
    #             str
    #         )

    # def testServerDataPathShouldBeStrAndReturn(self) -> None:
    #     config = Config()
    #     expected_value = '/somewhere/is/data-path'
    #     with mock.patch.dict(config.config, {'env': {'servers_data_path': expected_value}}):
    #         self.assertIsInstance(
    #             config.get_servers_data_path(),
    #             str
    #         )
    #         self.assertEqual(config.get_servers_data_path(), expected_value)

    # def testServerTemplatePathShouldBeStrAndReturn(self) -> None:
    #     config = Config()
    #     expected_value = '/somewhere/is/template-path'
    #     with mock.patch.dict(config.config, {'env': {'server_tpl_path': expected_value}}):
    #         self.assertEqual(config.get_server_template_path(), expected_value)
    #         self.assertIsInstance(
    #             config.get_server_template_path(),
    #             str
    #         )

    # def testSystemServiceUnitNameShouldBeStrAndReturn(self) -> None:
    #     config = Config()
    #     expected_value = 'minecraft-server.service'
    #     with mock.patch.dict(config.config, {'env': {'server_systemd_unit_name': expected_value}}):
    #         self.assertEqual(config.get_system_service_unit_name(), expected_value)
    #         self.assertIsInstance(
    #             config.get_system_service_unit_name(),
    #             str
    #         )