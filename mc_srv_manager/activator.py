#!/usr/bin/env python

import sys
from mc_srv_manager import server_manager

def activate_server(server_name: str) -> None:
    if not server_manager.check_if_server_exists(server_name):
        print(f"Server {server_name} doesn't exist!")
        sys.exit(1)

    if server_manager.is_server_running(server_name):
        server_manager.stop_server(server_name)

    # activate this server

    server_manager.start_server(server_name)
    print(f"Server {server_name} started succesfully!")
    sys.exit(0)