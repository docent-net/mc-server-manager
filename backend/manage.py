#!/usr/bin/env python

import os
import click
import mc_srv_manager.server_actions

@click.command()
@click.argument('action')
@click.option('--server_name', help="provide server name")
def main(action: str, server_name: str) -> None:
    """ 
    ACTION is one of: start, stop, restart, activate, info, create, secure
    
    """
    
    if action == 'activate':
        mc_srv_manager.server_actions.activate(server_name)
    elif action == 'create':
        mc_srv_manager.server_actions.create(server_name)
    elif action == 'info':
        mc_srv_manager.server_actions.show_servers_info()
    elif action == 'start':
        mc_srv_manager.server_actions.start()
    elif action == 'stop':
        mc_srv_manager.server_actions.stop()
    elif action == 'restart':
        mc_srv_manager.server_actions.restart()
    elif action == 'secure':
        mc_srv_manager.server_actions.secure_server_instance(server_name)


if __name__ == "__main__":
    main()