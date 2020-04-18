#!/usr/bin/env python

import os
import click
from mc_srv_manager.activator import activate_server
from mc_srv_manager.tester import test_environment

@click.command()
@click.argument('action')
@click.option('--server_name', required=True, help="provide server name")
def main(action: str, server_name: str) -> None:
    """ ACTION is one of: create_server, activate_server """
    
    if action == 'activate_server':
        activate_server(server_name)
    elif action == 'test':
        test_environment()


if __name__ == "__main__":
    main()