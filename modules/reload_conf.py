# reload_conf.py
import json
import os
import sys

def reload_config(base_dir, config_filename='config.json'):
    config_path = os.path.join(base_dir, config_filename)
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"Configuration reloaded: {config_path}")
        return config
    except Exception as e:
        print(f"Error reloading config: {e}")
        return None
