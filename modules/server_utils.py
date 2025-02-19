# server_utils.py

import sys
import os

def restart_flask():

    python = sys.executable
    os.execl(python, python, *sys.argv)  # restart service

def stop_flask(server_process):
    """Функція для зупинки Flask сервера"""
    print("Stopping Flask server...")
    server_process.terminate()  # stop
