import json
import os
from flask import Flask, send_from_directory, abort, Response
from werkzeug.utils import safe_join
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)

# Change the server header in Werkzeug
WSGIRequestHandler.server_version = "CoretexWEB/1.7.65A"
WSGIRequestHandler.sys_version = ""

# Load configuration
def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Generate a directory page with folders and files
def generate_directory_page(path, port):
    file_list = os.listdir(path)
    directories = [f for f in file_list if os.path.isdir(os.path.join(path, f))]
    files = [f for f in file_list if os.path.isfile(os.path.join(path, f))]

    html_content = "<h1>Directory Listing</h1><ul>"

    for directory in directories:
        # Create a relative path for directories
        rel_path = safe_join(path, directory)
        html_content += f'<li><a href="/{os.path.relpath(rel_path, "htdocs")}/">{directory}/</a></li>'

    for file in files:
        # Create a relative path for files
        rel_path = safe_join(path, file)
        html_content += f'<li><a href="/{os.path.relpath(rel_path, "htdocs")}">{file}</a></li>'

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

@app.route('/<path:filename>')
def serve_file(filename):
    file_path = os.path.join('htdocs', filename)

    # If it's a directory, check for the index file
    if os.path.isdir(file_path):
        index_file = config.get("index_file", "index.html")  # Get the index file name from the configuration
        index_path = os.path.join(file_path, index_file)  # Path to the index file in the current directory

        # If the index file exists, serve it
        if os.path.exists(index_path):
            return send_from_directory(file_path, index_file)

        # If no index file is found, show the directory contents
        return generate_directory_page(file_path, config["port"])

    # If it's a file, try to serve it
    try:
        return send_from_directory('htdocs', filename)
    except FileNotFoundError:
        abort(404)

@app.route('/')
def home():
    # Check if the specified index file exists
    index_file = config.get("index_file", "index.html")
    index_path = os.path.join('htdocs', index_file)

    if os.path.exists(index_path):
        return send_from_directory('htdocs', index_file)

    # If directory listing is disabled in the configuration
    if config.get("ftp_srv_index", "false") == "false":
        abort(404)  # or return a 404 error page

    # If no index file is found, show the directory listing
    return generate_directory_page('htdocs', config["port"])

if __name__ == '__main__':
    config = load_config('config.json')

    try:
        ssl_context = None
        if config.get("enable_ssl", False):
            ssl_context = (config["ssl_cert"], config["ssl_key"])

        print(f"CoretexWEB/1.7.65A - Running at port: {config['port']}")

        app.run(host=config["host"], port=config["port"], ssl_context=ssl_context)

    except Exception as e:
        print(f"Error occurred: {e}")