#!/usr/bin/env python

import sys

from mc_srv_manager.server_manager import server_manager


def test_environment() -> None:
    srv_mgr = server_manager()
    server_instances = srv_mgr.list_server_instances()
    if server_instances:
        print(f"Found {len(server_instances)} server(s):\n")
        print('\n'.join(f'{_srv}' for _srv in server_instances) + "\n")
    else:
        print("No server instances found. Create a new server?\n")

    active_server_name = srv_mgr.get_active_server_name()
    if active_server_name:
        print(f'Active server name: {active_server_name}\n')
    else:
        print(f'No active server found. Set an active server?\n')

    server_state = srv_mgr.is_server_running()
    if server_state is True:
        print('Server system service is running properly')
    else:
        print(f'Looks like server system service is stopped: {server_state}')

    sys.exit(0)