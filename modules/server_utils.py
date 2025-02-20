# server_utils.py

import sys
import os
import socket
import requests

def restart_flask():

    python = sys.executable
    os.execl(python, python, *sys.argv)  # restart service

def stop_flask(server_process):
    print("Stopping Flask server...")
    server_process.terminate()  # stop
    
def get_ip():
    try:
        global_ip = requests.get("https://api64.ipify.org").text
    except requests.exceptions.RequestException:
        global_ip = "An error has occurred. (Code: G1)"
    
    return f"Global: {global_ip}"