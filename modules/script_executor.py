import subprocess
import os
import json
from flask import request
import sys


def execute_python_script(script_path, query_string="", post_data=""):
    try:

        env = os.environ.copy()
        env["REQUEST_METHOD"] = "POST" if post_data else "GET"
        env["QUERY_STRING"] = query_string
        env["CONTENT_LENGTH"] = str(len(post_data)) if post_data else "0"
        env["CONTENT_TYPE"] = "application/x-www-form-urlencoded" if post_data else ""


        query_params = json.dumps(request.args.to_dict())


        result = subprocess.run(
            ["python", script_path, query_params],
            capture_output=True,
            text=True,
            env=env
        )


        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}", result.returncode if result.returncode != 0 else 200
    except Exception as e:
        return f"500 Internal Server Error: {e}", 500
