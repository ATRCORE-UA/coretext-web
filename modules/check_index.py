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

def find_index_file(directory, index_filename):
    index_path = os.path.join(directory, index_filename)
    if os.path.isfile(index_path):
        return index_filename
    return None