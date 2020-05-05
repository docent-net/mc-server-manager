#!/usr/bin/env python

from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
from flask import request
from mc_srv_manager.server_manager import server_manager

# configuration
DEBUG = True

app = FlaskAPI(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


server_manager = server_manager()

@app.route('/health', methods=['GET'])
def ping_pong():
    return {'status': 'OK'}

@app.route('/get_active_server', methods=['GET'])
def get_active_server():
    
    try:
        active_server = server_manager.get_active_server_name()
    except Exception as e:
        raise exceptions.ParseError(f'Could not fetch avtive server name: {e}')
    
    return {
        'status': 'success',
        'activeServer': active_server
    }

@app.route('/get_servers', methods=['GET'])
def get_servers():
    
    servers = []
    for srv_name in server_manager.list_server_instances():
        servers.append({'server_name': srv_name})

    servers = sorted(servers, key=lambda k: k['server_name']) 

    return {
        'status': 'success',
        'servers': servers
    }

@app.route('/create_server', methods=['PUT'])
def create_server():
    server_name = str(request.data.get('server_name', ''))
    if not server_name:
        raise exceptions.ParseError('No server_name provided?')

    if not server_manager.validate_server_name(server_name):
        raise exceptions.ParseError(f'Server name is incorrect or too long: {server_name}! Use only letters, numbers, underscores and hyphens!')

    if server_manager.check_if_server_exists(server_name):
        raise exceptions.ParseError(f'Server named {server_name} already exists!')

    try:
        server_manager.create_new_server_from_templ_dir(server_name)
    except Exception as e:
        raise exceptions.ParseError(f'Could not create a new server: {e}')

    return {
        'status': 'success',
        'message': 'Server created!'
    }

@app.route('/delete_server', methods=['DELETE'])
def delete_server():
    server_name = str(request.data.get('server_name', ''))
    if not server_name:
        raise exceptions.ParseError('No server_name provided?')

    if not server_manager.check_if_server_exists(server_name):
        raise exceptions.ParseError(f'Server named {server_name} doesn\'t exist!')

    # TODO: removing server
    raise exceptions.NotFound('Not implemented')

@app.route('/restart_server', methods=['POST','GET'])
def restart_server():
    """
    This method runs whole flow of restarting a server
    """

    if server_manager.is_server_running():
        try:
            server_manager.stop_server()
        except Exception as e:
            raise exceptions.ParseError(f'Could not stop server: {e}')
 
    try:
        server_manager.start_server()
    except Exception as e:
        raise exceptions.ParseError(f'Could not start server: {e}')

    return {
        'status': 'success',
        'message': 'Server restarted!'
    }
    
@app.route('/activate_server', methods=['POST','GET'])
def activate_server():
    """
    This method runs whole flow of activating a new server
    """
    server_name = str(request.data.get('server_name', ''))
    if not server_name:
        raise exceptions.ParseError('No server_name provided?')

    if not server_manager.check_if_server_exists(server_name):
        raise exceptions.ParseError(f'Server named {server_name} doesn\'t exist!')

    if server_manager.is_server_running():
        server_manager.stop_server()

     # activate this server
    if server_manager.remove_current_version_symlinks():
        if not server_manager.create_new_version_symlinks(server_name):
            raise exceptions.ParseError("Can't create symlinks!")
    else:
        raise exceptions.ParseError("Can't remove symlinks to the current version of the server")

    if server_manager.start_server():
        return {
            'status': 'success',
            'message': 'Server activated!'
        }
    else:
        raise exceptions.ParseError('Server was activated but could not be started')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)