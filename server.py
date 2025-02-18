import json
import os
import sys
from flask import Flask, send_from_directory, abort, Response
from werkzeug.utils import safe_join
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

# Change the server header in Werkzeug
WSGIRequestHandler.server_version = "CoretexWEB/1.7.65A"
WSGIRequestHandler.sys_version = ""

# Load configuration from a JSON file
def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Get the base directory path (for both .exe and Python script)
def get_base_dir():
    if getattr(sys, 'frozen', False):  # If the script is running as a .exe
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))  # If running as a Python script

# Generate a directory listing page
def generate_directory_page(path, port):
    file_list = os.listdir(path)
    directories = [f for f in file_list if os.path.isdir(os.path.join(path, f))]
    files = [f for f in file_list if os.path.isfile(os.path.join(path, f))]

    html_content = "<h1>Directory Listing</h1><ul>"

    # Add directories to the HTML content
    for directory in directories:
        rel_path = safe_join(path, directory)
        html_content += f'<li><a href="/{os.path.relpath(rel_path, config["htdocs_path"])}/">{directory}/</a></li>'

    # Add files to the HTML content
    for file in files:
        rel_path = safe_join(path, file)
        html_content += f'<li><a href="/{os.path.relpath(rel_path, config["htdocs_path"])}">{file}</a></li>'

    html_content += "</ul>"
    html_content += f'<hr><p>CoretexWEB/1.7.65A - Running at port: {port}</p>'

    response = Response(html_content, content_type="text/html")
    response.headers["X-Powered-By"] = "ATRCORE/Python"
    return response

# Add headers to all responses
@app.after_request
def add_headers(response):
    response.headers["X-Powered-By"] = "ATRCORE/Python"
    return response

# Route to serve files or directory listings
@app.route('/<path:filename>')
def serve_file(filename):
    file_path = os.path.join(config["htdocs_path"], filename)

    # If the path is a directory, check for an index file
    if os.path.isdir(file_path):
        index_file = config.get("index_file", "index.html")
        index_path = os.path.join(file_path, index_file)

        # If an index file exists, serve it
        if os.path.exists(index_path):
            return send_from_directory(file_path, index_file)

        # If no index file is found, generate a directory listing
        return generate_directory_page(file_path, config["port"])

    # If the path is a file, try to serve it
    try:
        return send_from_directory(config["htdocs_path"], filename)
    except FileNotFoundError:
        abort(404)

# Route for the root URL
@app.route('/')
def home():
    index_file = config.get("index_file", "index.html")
    index_path = os.path.join(config["htdocs_path"], index_file)

    # If the index file exists, serve it
    if os.path.exists(index_path):
        return send_from_directory(config["htdocs_path"], index_file)

    # If directory listing is disabled, return a 404 error
    if config.get("ftp_srv_index", "false") == "false":
        abort(404)

    # If no index file is found, generate a directory listing
    return generate_directory_page(config["htdocs_path"], config["port"])

if __name__ == '__main__':
    # Get the base directory and load the configuration
    base_dir = get_base_dir()
    config_path = os.path.join(base_dir, 'config.json')
    config = load_config(config_path)

    # Set the path to the htdocs directory from the configuration
    config["htdocs_path"] = os.path.join(base_dir, config.get("htdocs_path", "htdocs"))

    try:
        # Set up SSL if enabled in the configuration
        ssl_context = None
        if config.get("enable_ssl", False):
            ssl_context = (config["ssl_cert"], config["ssl_key"])

        # Print server information
        print(f"CoretexWEB/1.7.65A - Running at port: {config['port']}")
        print(f"Serving files from: {config['htdocs_path']}")

        # Start the Flask app
        app.run(host=config["host"], port=config["port"], ssl_context=ssl_context)

    except Exception as e:
        print(f"Error occurred: {e}")