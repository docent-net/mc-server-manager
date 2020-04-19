#!/usr/bin/env python

from pathlib import Path
from typing import Type, List
from pystemd.systemd1 import Unit
from pystemd.dbuslib import DBus
from mc_srv_manager.config import Config


class server_manager:
    def __init__(self) -> None:
        self.__config = Config()
        self.__current_server_version = self.get_active_server_name()

    def check_if_server_exists(self, srv_name: str) -> bool:
        if Path(
            self.__config.get_servers_data_path(),
            srv_name
        ).exists():
            return True 

        return False

    def __load_server_unit(self) -> Type[Unit]:
        with DBus(user_mode=True) as bus, \
            Unit(self.__config.get_system_service_unit_name(), bus=bus) as service:
            service.load()
            self.__service = service

    def is_server_running(self) -> bool:
        with DBus(user_mode=True) as bus, \
            Unit(self.__config.get_system_service_unit_name(), bus=bus) as service:
            service.load()
            if service.Unit.ActiveState == b'active':
                return True
            
            return service.Unit.ActiveState
        
        return False

    def stop_server(self) -> bool:
        try:
            unit.Stop(b"replace")
        except Exception as e:
            print(f"Can't stop server: {e}")
            return False

        return True

    def start_server(self) -> bool:
        # TODO: pystemd fix
        try:
            unit.Start(b"replace")
        except Exception as e:
            print(f"Can't start server: {e}")
            return False

        return True

    def get_srv_template_files(self) -> Type[List]:
        """ Method returns list of all files (top-level) and dirs
        from a server template """

        files = []
        pathlist = Path(self.__config.get_server_template_path()).glob('*')
        for path in pathlist:
            files.append(str(path))
        return files

    def get_active_server_name(self) -> str:
        """ 
        This method returns server that is currently set as active. Method
        checks the target directory of a server.properties symlink.
        """

        srv_symlink = Path(f'{self.__config.get_server_path()}/server.propertiess')
        
        try:
            srv_symlink_destination = srv_symlink.resolve(True)
        # If symlink was not found then there is no active server
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Can't get active server name: {e}")
            return False

        return str(srv_symlink_destination)


    def list_server_instances(self) -> Type[List]:
        """ 
        This method iterates over servers-data directory and 
        returns list of found servers.
        """

        # TODO: verify whether each server's files are in sync with server
        # template (nothing is missing)

        files = []
        pathlist = Path(self.__config.get_servers_data_path()).glob('*')
        for path in pathlist:
            files.append(str(path))
        return files

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

        # TODO: update current server version
        
        return True

    def remove_current_version_symlinks() -> None:
        """ This method removes symlinks pointing at current server
        version """

        # TODO: update current server version
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