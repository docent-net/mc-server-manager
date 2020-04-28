#!/usr/bin/env python

from unittest import TestCase, main, mock
from pathlib import Path
from mc_srv_manager.server_manager import server_manager


class testConfig(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

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