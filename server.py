from flask import Flask, request, send_from_directory, jsonify
import json
from werkzeug.serving import WSGIRequestHandler
from werkzeug.serving import run_simple
from werkzeug.middleware.proxy_fix import ProxyFix
from datetime import datetime
import sys
import os
import threading
import socket
import multiprocessing
import signal
import logging
import time

ver = "1.7.71B"

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from directory_listing import generate_directory_page
import reload_conf
from server_utils import *
from actions import *
from check_index import *

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

WSGIRequestHandler.server_version = f"CoretexWEB/{ver}"
WSGIRequestHandler.sys_version = ""

# base_dir
def get_base_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

# load config
def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}

# logs
@app.before_request
def log_request():
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)

    # Check if logging is enabled in config
    logs_enabled = config.get("logs", "false").lower() == "true"
    
    if logs_enabled:
        with open("access_log.txt", "a") as log_file:
            log_file.write(f'{request.remote_addr} accessed {request.path} at {datetime.now()}\n')


@app.route('/', defaults={'subpath': ''}, methods=["GET"])
@app.route('/<path:subpath>', methods=["GET"])
def serve_directory(subpath):
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)

    htdocs_path = os.path.join(base_dir, config.get("htdocs_path", "htdocs"))
    requested_path = os.path.join(htdocs_path, subpath.strip("/"))
    index_filename = config.get("index_file", "index.html")
    ftp_srv_index = str(config.get("ftp_srv_index", "false")).lower() == "true"

    if os.path.isdir(requested_path):
        index_file = find_index_file(requested_path, index_filename)

        if index_file:
            return send_from_directory(requested_path, index_file)

        if ftp_srv_index:
            base_url = f"/{subpath.strip('/')}"
            return generate_directory_page(requested_path, config["port"], base_url, ver)

        return "404 Not found - index_file was not found", 404

    elif os.path.isfile(requested_path):
        return send_from_directory(htdocs_path, subpath.strip("/"))

    return "404 Not Found", 404


def listen_for_commands(server_process):

    while True:
        command = input("Enter command: ")
        if command == "reload_conf":
            base_dir = get_base_dir()
            config = reload_conf.reload_config(base_dir)
            if config:
                print("Configuration reloaded successfully. Restarting CortextWEB/" + ver + " server...")
                restart_flask()
            else:
                print("Failed to reload configuration.")
        elif command == "stop":
            stop_flask(server_process)
        elif command == "":
            command = input("Enter command: ")
        elif command == "exit":
            print("Exiting...")
            break
        else:
            print(f"Unknown command: {command}")

def run_flask_server():
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)
    htdocs_path = os.path.join(base_dir, config.get("htdocs_path", "htdocs"))

    try:
        ssl_context = None
        if config.get("enable_ssl", False):
            ssl_context = (config["ssl_cert"], config["ssl_key"])

        print("\n" + "="*50)
        print(f"CoretexWEB/{ver}")
        print(f"Running at port: {config['port']}")
        print(f"Serving files from: {htdocs_path}")
        if ssl_context:
            print(f"SSL Enabled: Yes")
        else:
            print(f"SSL Enabled: No")
        print("="*50)

        run_simple(config["host"], config["port"], app, ssl_context=ssl_context, use_reloader=False)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    server_process = multiprocessing.Process(target=run_flask_server)
    server_process.start()
    time.sleep(5)

    listen_for_commands(server_process)
