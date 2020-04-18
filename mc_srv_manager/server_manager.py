#!/usr/bin/env python

from pathlib import Path
from typing import Type, List
from pystemd.systemd1 import Unit
from mc_srv_manager.config import Config

config = Config()

def check_if_server_exists(srv_name: str) -> bool:
    if Path(
        config.get_servers_data_path(),
        srv_name
    ).exists():
        return True 

    return False

def verify_system_unit_is_loadable(srv_name: str) -> Type[Unit]:
    unit_name = config.get_system_service_unit_name()
    
    # TODO: verify this works with user services
    try:
        unit = Unit(b'ddd.service')
    except Exception:
        raise Exception(f"Can't load service {unit_name}!")
        print(unit)
    unit.load()
    
    return unit

def is_server_running(srv_name: str) -> bool:
    try:
        unit = verify_system_unit_is_loadable(srv_name)
    except Exception:
        return False
    
    if unit.Unit.ActiveState == b'active':
        return True
    
    return False

def stop_server(srv_name: str) -> bool:
    try:
        unit = verify_system_unit_is_loadable(srv_name)
    except Exception:
        return False
    
    try:
        unit.Stop(b"replace")
    except Exception as e:
        print(f"Can't stop server {srv_name}: {e}")
        return False

    return True

def start_server(srv_name: str) -> bool:
    if not verify_system_unit_is_loadable(srv_name):
        return False
    
    try:
        unit.Start(b"replace")
    except Exception as e:
        print(f"Can't start server {srv_name}: {e}")
        return False

    return True

def get_srv_template_files() -> Type[List]:
    """ Method returns list of all files (top-level) and dirs
    from a server template """

    files = []
    pathlist = Path(config.get_server_template_path()).glob('*')
    for path in pathlist:
        files.append(str(path))
    return files

def get_active_server_name() -> str:
    """ 
    This method returns server that is currently set as active. Method
    checks the target directory of a server.properties symlink.
    """

    srv_symlink = Path(f'{config.get_server_path()}/server.propertiess')
    
    try:
        srv_symlink_destination = srv_symlink.resolve(False)
    except Exception as e:
        print(f"Can't get active server name: {e}")
        return False

    return str(srv_symlink_destination)


def list_server_instances() -> Type[List]:
    """ 
    This method iterates over servers-data directory and 
    returns list of found servers.
    """

    # TODO: verify whether each server's files are in sync with server
    # template (nothing is missing)

    return ['123', '234']
    # files = []
    # pathlist = Path(config.get_servers_data_path()).glob('*')
    # for path in pathlist:
    #     files.append(str(path))
    # return files