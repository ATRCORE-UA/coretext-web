from flask import Flask, request, send_from_directory, jsonify, redirect
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


ver = "1.7.74S"

sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))
from directory_listing import generate_directory_page
import reload_conf
from server_utils import *
from actions import *
from check_index import *
from htaccess import check_htaccess_in_all_directories, read_htaccess
from script_executor import execute_python_script
from ddos_protection import check_ip


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

# Set the server version before initializing the Flask app
python_version = sys.version.split()[0]
config_path = os.path.join(get_base_dir(), 'config.json')
config = load_config(config_path)
enable_py_scripts = config.get("py-scripts", False)

if enable_py_scripts:
    WSGIRequestHandler.server_version = f"CoretexWEB/{ver} Python/{python_version}"
else:
    WSGIRequestHandler.server_version = f"CoretexWEB/{ver}"
WSGIRequestHandler.sys_version = ""

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

# logs
@app.before_request
def log_request():
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)

    logs_enabled = str(config.get("logs", "false")).lower() == "true"
    
    if logs_enabled:
        with open("access_log.txt", "a") as log_file:
            log_file.write(f'{request.remote_addr} accessed {request.path} at {datetime.now()}\n')

def block_ddos():
    enable_ddos = config.get("ddos-protection", False)
    if enable_ddos:
        if not check_ip(request.remote_addr):
            return "429 Too Many Requests", 429



@app.route('/', defaults={'subpath': ''}, methods=["GET"])
@app.route('/<path:subpath>', methods=["GET"])
def serve_directory(subpath):
    # Додаємо захист від DDoS
    response = block_ddos()
    if response:
        return response
    
    # Завантажуємо конфігурацію та шляхи
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)

    htdocs_path = os.path.join(base_dir, config.get("htdocs_path", "htdocs"))
    requested_path = os.path.join(htdocs_path, subpath.strip("/"))
    index_filename = config.get("index_file", "index.html")  # Отримуємо параметр index_file з конфігурації
    ftp_srv_index = str(config.get("ftp_srv_index", "false")).lower() == "true"
    enable_py_scripts = config.get("py-scripts", False)

    # Перевірка на htaccess
    htaccess_result = check_htaccess_in_all_directories(requested_path)
    if htaccess_result:
        if isinstance(htaccess_result, tuple):
            if htaccess_result[0].startswith(("http://", "https://")):
                return redirect(htaccess_result[0])
            return htaccess_result[0], htaccess_result[1]
        return redirect(htaccess_result)

    htaccess_rules = read_htaccess(requested_path)
    if htaccess_rules:
        for rule in htaccess_rules:
            rule = rule.strip()
            if rule.startswith("Redirecttourl"):
                _, url = rule.split(maxsplit=1)
                return redirect(url)

    # Якщо запитаний шлях - це директорія
    if os.path.isdir(requested_path):
        if htaccess_rules and "Options -Indexes" in "".join(htaccess_rules):
            return "403 Forbidden - Directory listing is disabled", 403

        # Якщо запитаний файл - Python-скрипт
        if index_filename.endswith(".py"):
            if os.path.isfile(os.path.join(requested_path, index_filename)):
                if enable_py_scripts:
                    return execute_python_script(os.path.join(requested_path, index_filename))
                return "403 Forbidden: Python script execution is disabled.", 403
        else:
            index_file = find_index_file(requested_path, index_filename)
            if index_file:
                return send_from_directory(requested_path, index_file)

        # Генерація сторінки директорії для FTP-сервера
        if ftp_srv_index:
            base_url = f"/{subpath.strip('/')}"
            return generate_directory_page(requested_path, config["port"], base_url, ver)

        return "404 Not found - index_file was not found", 404

    # Якщо запитаний шлях - це файл
    elif os.path.isfile(requested_path):
        if requested_path.endswith(".py"):
            if enable_py_scripts:
                return execute_python_script(requested_path)
            return "403 Forbidden: Python script execution is disabled.", 403
        return send_from_directory(htdocs_path, subpath.strip("/"))

    return "404 Not Found", 404




def listen_for_commands(server_process):
    while True:
        command = input("Enter command: ").strip().lower()
        
        if command == "reload_conf":
            base_dir = get_base_dir()
            config = reload_conf.reload_config(base_dir)
            if config:
                print(f"Configuration reloaded successfully. Restarting CoretexWEB/{ver} server...")
                restart_flask()
            else:
                print("Failed to reload configuration.")
        elif command == "stop":
            print("Stopping server...")
            server_process.terminate()
            break
        elif command == "ip_conf":
            ips = get_ip().split("\n")
            for ip in ips:
                print(ip)
        elif command == "exit":
            print("Exiting...")
            server_process.terminate()
            sys.exit(0)
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
        print(f"Running at port: {config.get('port', 5000)}")
        print(f"Serving files from: {htdocs_path}")
        print(f"Python scripts execution: {'Enabled' if config.get('py-scripts', False) else 'Disabled'}")
        print(f"SSL Enabled: {'Yes' if ssl_context else 'No'}")
        print("="*50)

        run_simple(config.get("host", "127.0.0.1"), config.get("port", 5000), app, ssl_context=ssl_context, use_reloader=False)
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == '__main__':
    server_process = multiprocessing.Process(target=run_flask_server)
    server_process.start()
    time.sleep(2)
    listen_for_commands(server_process)
