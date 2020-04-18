#!/usr/bin/env python

import sys

from mc_srv_manager.server_manager import list_server_instances
from mc_srv_manager.server_manager import get_active_server_name
from mc_srv_manager.server_manager import is_server_running

def test_environment() -> None:
    server_instances = list_server_instances()
    if server_instances:
        print(f"Found {len(server_instances)} server(s):\n")
        print('\n'.join(f'{_srv}' for _srv in server_instances) + "\n")
    else:
        print("No server instances found. Create a new server?\n")

    active_server_name = get_active_server_name()
    if active_server_name:
        print(f'Active server name: {active_server_name}\n')
    else:
        print(f'No active server found. Set an active server?\n')

    server_state = is_server_running()
    if server_state is True:
        print('Server system service is running properly')
    else:
        print(f'Looks like server system service is stopped: {server_state}')

    sys.exit(0)