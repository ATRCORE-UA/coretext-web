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

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def load_config(filename):
    with open(filename, 'r') as f:
        return json.load(f)

