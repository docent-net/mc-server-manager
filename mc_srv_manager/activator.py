#!/usr/bin/env python

import sys
from mc_srv_manager.server_manager import server_manager
from pathlib import Path


srv_mgr = server_manager()

def activate_server(server_name: str) -> None:
    if not srv_mgr.check_if_server_exists(server_name):
        print(f"Server {server_name} doesn't exist!")
        sys.exit(1)
    
    if srv_mgr.is_server_running():
        srv_mgr.stop_server()

    # activate this server
    if srv_mgr.remove_current_version_symlinks():
        if not srv_mgr.create_new_version_symlinks(server_name):
            print("Can't create symlinks!")
            sys.exit(1)
        else:
            print('New version symlinked succesfully!')
    else:
        print("Can't remove symlinks to the current version of the server!")
        sys.exit(1)

    if srv_mgr.start_server():
        print(f"Server {server_name} started succesfully!")
    else:
        sys.exit(1)

    active_server_name = srv_mgr.get_active_server_name()
    if active_server_name:
        print(f'Active server name: {active_server_name}\n')
    else:
        print(f'No active server found. Set an active server?\n')
        
    sys.exit(0)