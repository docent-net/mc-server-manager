#!/usr/bin/env python

from pathlib import Path
from typing import Type, List
import re
from pystemd.systemd1 import Unit
from pystemd.dbuslib import DBus
from mc_srv_manager.config import Config
from mc_srv_manager.utils import copytree


class server_manager:
    def __init__(self) -> None:
        self.__config = Config()
        self.__current_server_name = self.__read_active_server_name()

    def check_if_server_exists(self, srv_name: str) -> bool:
        if Path(
            self.__config.get_servers_data_path(),
            srv_name
        ).exists():
            return True 

        return False

    def is_server_running(self) -> bool:
        with DBus(user_mode=True) as bus, \
            Unit(self.__config.get_system_service_unit_name(), \
            bus=bus, _autoload=True) as service:
    
            if service.Unit.ActiveState == b'active':
                return True

            return False

        print('Can\t read server state via Dbus!')
        return False

    def stop_server(self) -> bool:
        with DBus(user_mode=True) as bus, \
            Unit(self.__config.get_system_service_unit_name(), \
            bus=bus, _autoload=True) as service:
    
            try:
                service.Unit.Stop(b"replace")
            except Exception as e:
                print(f"Can't stop server: {e}")
                return False

            return True

        print('Can\t read server state via Dbus!')
        return False

    def start_server(self) -> bool:
        with DBus(user_mode=True) as bus, \
            Unit(self.__config.get_system_service_unit_name(), \
            bus=bus, _autoload=True) as service:
    
            try:
                service.Unit.Start(b"replace")
            except Exception as e:
                print(f"Can't start server: {e}")
                return False

            # print(f'Server\'s state: {service.Unit.ActiveState}')    
            return True

        print('Can\t read server state via Dbus!')
        return False

    def validate_server_name(self, srv_name: str) -> bool:
        """ Method checks whether server name consists of allowed
        characters only """

        if len(srv_name) > 32:
            return False

        regexp = re.compile('[^0-9a-zA-Z_-]+')
        if regexp.search(srv_name):
            return False

        return True

    def get_srv_template_files(self) -> Type[List]:
        """ Method returns list of all files (top-level) and dirs
        from a server template """

        files = []
        pathlist = Path(self.__config.get_server_template_path()).glob('*')
        for path in pathlist:
            files.append(str(path.name))
        return files

    def get_active_server_name(self) -> str:
        """ 
        This method returns server that is currently set as active
        """

        return self.__current_server_name

    def __update_current_server_name(self, server_name:str = False) -> None:
        """
        This method updates state information about server, which is
        currently symlinked
        """
        if server_name:
            self.__current_server_name = server_name
        else:
            self.__current_server_name = self.__read_active_server_name()

    def __read_active_server_name(self) -> str:
        """
        This method guesses (basing on server.properties symlink) currently
        active server name
        """

        srv_symlink = Path(f'{self.__config.get_server_path()}/server.properties')
        
        try:
            srv_symlink_destination = srv_symlink.resolve(True)
        # If symlink was not found then there is no active server
        except FileNotFoundError:
            return False
        except Exception as e:
            print(f"Can't get active server name: {e}")
            return False

        return str(srv_symlink_destination.parent.name)

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
            files.append(str(path.name))
        return files

    def create_new_version_symlinks(self, server_name: str) -> bool:
        """ This method removes symlinks pointing at current server
        version """

        files = self.get_srv_template_files()

        for file in files:
            file_obj = Path(self.__config.get_server_path(), file)
            if not file_obj.exists():
                try:
                    server_path = f'{self.__config.get_servers_data_path()}/{server_name}/{file}'
                    # print(f'Creating symlink from {str(file_obj)} to {server_path}')
                    file_obj.symlink_to(server_path)
                except Exception:
                    print(f"Cant't create symlink for {server_path}!")
                    return False
            else:
                print(f"Looks like symlink {str(file_obj)} already exist!")
                return False

        self.__update_current_server_name(server_name)

        return True

    def remove_current_version_symlinks(self) -> bool:
        """ This method removes symlinks pointing at current server
        version """

        symlinks = self.get_srv_template_files()

        # in case no symlinks found - probably 1st server being created
        if not symlinks:
            return True

        for file in symlinks:
            file_obj = Path(self.__config.get_server_path(), file)
            try:
                # print(f'Removing file {file_obj}')
                file_obj.unlink(missing_ok = True)
            except Exception:
                print(f"Cant't remove dir {file}!")
                return False

        self.__update_current_server_name('none')

        return True

    def create_new_server_from_templ_dir(self, server_name: str) -> bool:
        """ 
        This method creates a new server by copying template directory 
        into a new server-data/<server_name> dir
        """

        try:
            copytree(
                src=self.__config.get_server_template_path(),
                dst=f'{self.__config.get_servers_data_path()}/{server_name}'
            )
        except Exception as e:
            print(f"Cant't create new server {server_name}: {e}!")
            return False
        
        return True