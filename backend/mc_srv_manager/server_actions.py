#!/usr/bin/env python

import sys
from mc_srv_manager.server_manager import server_manager
from pathlib import Path


srv_mgr = server_manager()

def activate(server_name: str) -> None:
    """
    This method runs whole flow of activating a new server
    """

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

def start() -> None:
    """
    This method runs flow of starting server instance (system service)
    """
    
    active_server_name = srv_mgr.get_active_server_name()
    if not active_server_name:
        print(f'No active server found. Set an active server?\n')
        sys.exit(1)
    
    if srv_mgr.is_server_running():
        print(f'Looks like this server {active_server_name} is already running. Use restart instead of start.')
        sys.exit(1)

    if srv_mgr.start_server():
        print(f"Server {active_server_name} started succesfully!")
        sys.exit(0)

    print(f"Server {active_server_name} could not be started!")
    sys.exit(1)

def stop() -> None:
    """
    This method runs flow of stopping server instance (system service)
    """
    
    active_server_name = srv_mgr.get_active_server_name()
    if not active_server_name:
        print(f'No active server found. Set an active server?\n')
        sys.exit(1)
    
    if not srv_mgr.is_server_running():
        print(f'Looks like this server {active_server_name} is already stopped.')
        sys.exit(1)

    if srv_mgr.stop_server():
        print(f"Server {active_server_name} stopped succesfully!")
        sys.exit(0)

    print(f"Server {active_server_name} could not be stopped!")
    sys.exit(1)

def restart() -> None:
    """
    This method runs flow of restarting server instance (system service)
    """
    
    active_server_name = srv_mgr.get_active_server_name()
    if not active_server_name:
        print(f'No active server found. Set an active server?\n')
        sys.exit(1)
    
    if srv_mgr.is_server_running():
        if srv_mgr.stop_server():
            print(f"Server {active_server_name} stopped succesfully!")
        else:
            print(f"Server {active_server_name} could not be stopped!")
            sys.exit(1)

    if srv_mgr.start_server():
        print(f"Server {active_server_name} started succesfully!")
        sys.exit(0)
    else:
        print(f"Server {active_server_name} could not be started!")
        sys.exit(1)

    sys.exit(1)

def create(server_name: str) -> None:
    """
    This method runs whole flow of creating a new server from a template
    """

    if srv_mgr.check_if_server_exists(server_name):
        print(f"Server {server_name} already exist!")
        sys.exit(1)
    
    # create new server
    if srv_mgr.create_new_server_from_templ_dir(server_name):
        print('New server created successfully!')
    else:
        print("Can't create new server!")
        sys.exit(1)

    active_server_name = srv_mgr.get_active_server_name()
    if active_server_name:
        print(f'Active server name: {active_server_name}\n')
    else:
        print(f'No active server found. Set an active server?\n')
        
    sys.exit(0)

def show_servers_info() -> None:
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

def secure_server_instance(server_name: str) -> None:
    """
    This method runs whole flow of securing a server instance
    """
    srv_mgr = server_manager()

    if not srv_mgr.check_if_server_exists(server_name):
        print(f"Server {server_name} doesn't exist!")
        sys.exit(1)

    # secure this server
    if srv_mgr.secure_server_instance(server_name):
        print('Server instance secured!')
        sys.exit(0)
    else:
        print("Could not secure this server instance!")
        sys.exit(1)