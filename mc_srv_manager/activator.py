#!/usr/bin/env python

import sys
from mc_srv_manager import server_manager
from pathlib import Path

def activate_server(server_name: str) -> None:
    if not server_manager.check_if_server_exists(server_name):
        print(f"Server {server_name} doesn't exist!")
        sys.exit(1)
    
    if server_manager.is_server_running(server_name):
        server_manager.stop_server(server_name)

    # activate this server
    if remove_current_version_symlinks():
        if not create_new_version_symlinks(server_name):
            print("Can't create symlinks!")
            sys.exit(1)
        else:
            print('New version symlinked sccesfully!')
    else:
        print("Can't remove symlinks to the current version of the server!")
        sys.exit(1)

    if server_manager.start_server(server_name):
        print(f"Server {server_name} started succesfully!")
    else:
        sys.exit(1)
        
    sys.exit(0)

def create_new_version_symlinks(server_name: str) -> None:
    """ This method removes symlinks pointing at current server
    version """

    # WIP
    # TODO: this doesn't work yet

    files = server_manager.get_srv_template_files()
    print(files)

    for file in files:
        print(file)
        file_obj = Path(server_manager.config.get_server_template_path(), file)
        if not file_obj.exists():
            try:
                server_path = f'{server_manager.config.get_servers_data_path()}/{server_name}/{file}'
                file_obj.symlink_to(server_path)
            except Exception:
                print(f"Cant't create symlink for {server_path}!")
                return False
        else:
            print(f"Looks like symlink {str(file_obj)} already exist!")
            return False

    return True

def remove_current_version_symlinks() -> None:
    """ This method removes symlinks pointing at current server
    version """

    symlinks = server_manager.get_srv_template_files()

    # in case no symlinks found - probably 1st server being created
    if not symlinks:
        return True

    for file in symlinks:
        file_obj = Path(server_manager.config.get_server_template_path(), file)
        if file_obj.is_dir():
            try:
                file_obj.rmdir()
            except Exception:
                print(f"Cant't remove file {file}!")
                sys.exit(1)
        else:
            try:
                file_obj.unlink(missing_ok = True)
            except Exception:
                print(f"Cant't remove dir {file}!")
                sys.exit(1)

    return True