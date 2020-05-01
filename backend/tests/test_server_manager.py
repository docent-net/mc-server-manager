#!/usr/bin/env python

from unittest import TestCase, main, mock
from pathlib import Path
from mc_srv_manager.server_manager import server_manager


def bogus_return_function(self):
    return '/somewhere/in/the/os';
    
class testConfig(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    @mock.patch('mc_srv_manager.config.Config.get_servers_data_path', bogus_return_function)
    @mock.patch('mc_srv_manager.config.Config.get_server_path', bogus_return_function)
    def testServerExistance(self) -> None:
        srv_manager = server_manager()
        with mock.patch.object(Path, 'exists') as mock_exists:
            mock_exists.return_value = False
            self.assertEqual(
                            srv_manager.check_if_server_exists('bous_server'),
                            False
                            )
            mock_exists.return_value = True
            self.assertEqual(
                            srv_manager.check_if_server_exists('bous_server'),
                            True
                            )