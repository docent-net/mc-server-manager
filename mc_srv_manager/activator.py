#!/usr/bin/env python

import sys
from mc_srv_manager import server_manager
from mc_srv_manager import config
from pathlib import Path

srv_mgr = server_manager()

def activate_server(server_name: str) -> None:
    if not srv_mgr.check_if_server_exists(server_name):
        print(f"Server {server_name} doesn't exist!")
        sys.exit(1)
    
    if srv_mgr.is_server_running(server_name):
        srv_mgr.stop_server(server_name)

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

    if srv_mgr.start_server(server_name):
        print(f"Server {server_name} started succesfully!")
    else:
        sys.exit(1)
        
    sys.exit(0)

# TODO: this method should be moved to server_manager
def create_new_version_symlinks(server_name: str) -> None:
    """ This method removes symlinks pointing at current server
    version """

    # WIP
    # TODO: this doesn't work yet

    files = srv_mgr.get_srv_template_files()
    print(files)

    for file in files:
        print(file)
        file_obj = Path(srv_mgr.config.get_server_template_path(), file)
        if not file_obj.exists():
            try:
                server_path = f'{srv_mgr.config.get_servers_data_path()}/{server_name}/{file}'
                file_obj.symlink_to(server_path)
            except Exception:
                print(f"Cant't create symlink for {server_path}!")
                return False
        else:
            print(f"Looks like symlink {str(file_obj)} already exist!")
            return False

    return True

# TODO: this method should be moved to server_manager
def remove_current_version_symlinks() -> None:
    """ This method removes symlinks pointing at current server
    version """

    symlinks = srv_mgr.get_srv_template_files()

    # in case no symlinks found - probably 1st server being created
    if not symlinks:
        return True

    for file in symlinks:
        file_obj = Path(srv_mgr.config.get_server_template_path(), file)
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