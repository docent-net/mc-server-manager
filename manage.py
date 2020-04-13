#!/usr/bin/env python

import click
from mc_srv_manager.activator import activate_server

@click.command()
@click.argument('action')
@click.option('--server_name', required=True, help="provide server name")
def main(action: str, server_name: str) -> None:
    """ ACTION is one of: create_server, activate_server """
    
    if action == 'activate_server':
        activate_server(server_name)


if __name__ == "__main__":
    main()