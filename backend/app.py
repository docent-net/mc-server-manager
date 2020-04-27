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

@app.route('/get_servers', methods=['GET'])
def get_servers():
    
    servers = []
    for srv_name in server_manager.list_server_instances():
        servers.append({'server_name': srv_name})

    return {
        'status': 'success',
        'servers': servers
    }

@app.route('/create_server', methods=['PUT'])
def create_server():
    server_name = str(request.data.get('server_name', ''))
    if not server_name:
        raise exceptions.ParseError('No server_name provided?')

    if server_manager.check_if_server_exists(server_name):
        raise exceptions.ParseError(f'Server named {server_name} already exists!')

    try:
        server_manager.create_new_server_from_templ_dir(server_name)
    except Exception as e:
        raise exceptions.ParseError(f'Could not create a new server: {e}')

    return {
        'status': 'server_created'
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)