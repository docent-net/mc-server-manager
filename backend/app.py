#!/usr/bin/env python

from flask_api import Flask-API, jsonify
from flask.ext.api.exceptions import APIException
from flask_cors import CORS
from mc_srv_manager.server_manager import server_manager

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


server_manager = server_manager()

@app.route('/health', methods=['GET'])
def ping_pong():
    return jsonify('OK')


@app.route('/get_servers', methods=['GET'])
def get_servers():
    
    servers = []
    for srv_name in server_manager.list_server_instances():
        servers.append({'server_name': srv_name})

    return jsonify({
        'status': 'success',
        'servers': servers
    })

@app.route('/activate_server/{server_name}', methods=['GET'])
def activate_servers(server_name):
    

    return jsonify({
        'status': 'success',
        'servers': servers
    })


if __name__ == '__main__':
    app.run()