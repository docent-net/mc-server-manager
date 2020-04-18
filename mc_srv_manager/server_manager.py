#!/usr/bin/env python

from pathlib import Path
from typing import Type, List
from pystemd.systemd1 import Unit
from pystemd.dbuslib import DBus
from mc_srv_manager.config import Config

config = Config()

def check_if_server_exists(srv_name: str) -> bool:
    if Path(
        config.get_servers_data_path(),
        srv_name
    ).exists():
        return True 

    return False

def is_server_running() -> bool:
    # TODO: having pystemd issue here; waiting for an answer: https://github.com/facebookincubator/pystemd/issues/52
    bus = DBus(user_mode=True)
    unit = Unit(b'minecraft-server-stub.service', bus=bus, _autoload=True)
    # unit.load()
    print(unit)
    print(unit.__dict__)
    print(dir(unit))
    if unit.Unit.ActiveState == b'active':
        return True
    
    return unit.Unit.ActiveState

def stop_server() -> bool:
    try:
        unit.Stop(b"replace")
    except Exception as e:
        print(f"Can't stop server: {e}")
        return False

    return True

def start_server() -> bool:
    try:
        unit.Start(b"replace")
    except Exception as e:
        print(f"Can't start server: {e}")
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
        srv_symlink_destination = srv_symlink.resolve(True)
    # If symlink was not found then there is no active server
    except FileNotFoundError:
        return False
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

    files = []
    pathlist = Path(config.get_servers_data_path()).glob('*')
    for path in pathlist:
        files.append(str(path))
    return files