import subprocess
import os
import sys


def execute_python_script(script_path, query_string="", post_data=""):
    try:

        env = os.environ.copy()
        env["REQUEST_METHOD"] = "POST" if post_data else "GET"
        env["QUERY_STRING"] = query_string
        env["CONTENT_LENGTH"] = str(len(post_data))
        env["CONTENT_TYPE"] = "application/x-www-form-urlencoded" if post_data else ""


        result = subprocess.run(
            [sys.executable, script_path],
            input=post_data,
            text=True,
            capture_output=True,
            env=env
        )


        return result.stdout, result.returncode if result.returncode != 0 else 200
    except Exception as e:
        return f"500 Internal Server Error: {e}", 500
