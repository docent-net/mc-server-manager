#!/usr/bin/env python

import sys

from mc_srv_manager.server_manager import list_server_instances
from mc_srv_manager.server_manager import get_active_server_name

def test_environment() -> None:
    server_instances = list_server_instances()
    if server_instances:
        print(f"Found {len(server_instances)} servers:\n")
        print('\n'.join(f'{_srv}' for _srv in server_instances))
    else:
        print("No server instances found. Create a new server?")

    active_server_name = get_active_server_name()
    if active_server_name:
        print(f'Active server name: {active_server_name}')
    else:
        print(f'Can\'t get active server: {active_server_name}')
        
    # TODO: print current server instance
    # TODO: print current server state

    print('It works!')
    sys.exit(1)