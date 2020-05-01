#!/usr/bin/env python

import os
import click
import mc_srv_manager.server_actions
from mc_srv_manager.tester import test_environment

@click.command()
@click.argument('action')
@click.option('--server_name', help="provide server name")
def main(action: str, server_name: str) -> None:
    """ 
    ACTION is one of: start, stop, restart, activate, test, create
    
    """
    
    if action == 'activate':
        mc_srv_manager.server_actions.activate(server_name)
    elif action == 'create':
        mc_srv_manager.server_actions.create(server_name)
    elif action == 'test':
        test_environment()
    elif action == 'start':
        mc_srv_manager.server_actions.start()
    elif action == 'stop':
        mc_srv_manager.server_actions.stop()
    elif action == 'restart':
        mc_srv_manager.server_actions.restart()


if __name__ == "__main__":
    main()