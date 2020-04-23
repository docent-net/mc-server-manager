#!/usr/bin/env python

from unittest import TestCase, main, mock
from mc_srv_manager.config import Config
from pathlib import PosixPath


class testConfig(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def testCfgPathShouldBePosixPath(self) -> None:
        config = Config()
        self.assertIsInstance(
            config.get_cfg_file_path(),
            PosixPath
        )

    def testServerPathShouldBeStr(self) -> None:
        config = Config()
        self.assertIsInstance(
            config.get_server_path(),
            str
        )

    def testShouldReturnServerPath(self) -> None:
        config = Config()
        expected_value = '/somewhere/is/server-path'
        with mock.patch.dict(config.config, {'env': {'server_path': expected_value}}):
            assert config.get_server_path() is expected_value

    def testServerDataPathShouldBeStr(self) -> None:
        config = Config()
        self.assertIsInstance(
            config.get_servers_data_path(),
            str
        )

    def testShouldReturnDataPath(self) -> None:
        config = Config()
        expected_value = '/somewhere/is/data-path'
        with mock.patch.dict(config.config, {'env': {'servers_data_path': expected_value}}):
            assert config.get_servers_data_path() is expected_value

    def testServerTemplatePathShouldBeStr(self) -> None:
        config = Config()
        self.assertIsInstance(
            config.get_server_template_path(),
            str
        )

    def testShouldReturnTemplatePath(self) -> None:
        config = Config()
        expected_value = '/somewhere/is/template-path'
        with mock.patch.dict(config.config, {'env': {'server_tpl_path': expected_value}}):
            assert config.get_server_template_path() is expected_value

    def testSystemServiceUnitNameShouldBeStr(self) -> None:
        config = Config()
        self.assertIsInstance(
            config.get_system_service_unit_name(),
            str
        )

    def testShouldReturnSystemServiceUnitName(self) -> None:
        config = Config()
        expected_value = 'minecraft-server.service'
        with mock.patch.dict(config.config, {'env': {'server_systemd_unit_name': expected_value}}):
            assert config.get_system_service_unit_name() is expected_value