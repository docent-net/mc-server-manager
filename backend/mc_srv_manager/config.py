#!/usr/bin/env python

import configparser
from pathlib import Path
from typing import Type
# 1
class Config:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read(str(self.get_cfg_file_path()))

    def get_cfg_file_path(self) -> Type[Path]: 
        """                                                                                                                                                                                                                                      
        This function returns full system path where Github config file                                                                                                                                                                          
        is expected                                                                                                                                                                                                                              
        """                                                                                                                                                                                                                                      
        return Path(f"{str(Path.home())}/.minecraft/mc-manager-config")

    def get_server_path(self) -> str:
        """
        This method returns path to the main instance of the
        game server.
        """
        try:
            srv_path = self.config['env']['server_path']
        except KeyError:
            raise ValueError('No env:server_path defined in config')

        return srv_path

    def get_servers_data_path(self) -> str:
        """
        This method returns path to the directory where data directories
        of all server instances are placed
        """
        
        try:
            data_path = self.config['env']['servers_data_path']
        except KeyError:
            raise ValueError('No env:servers_data_path defined in config')

        return data_path

    def get_server_template_path(self) -> str:
        try:
            tpl_path = self.config['env']['server_tpl_path']
        except KeyError:
            raise ValueError('No env:server_tpl_path defined in config')

        return tpl_path

    def get_system_service_unit_name(self) -> str:
        try:
            unit_name = self.config['env']['server_systemd_unit_name']
        except KeyError:
            raise ValueError('No env:server_systemd_unit_name defined in config')

        return unit_name