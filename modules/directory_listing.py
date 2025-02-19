import os
from flask import Response
from datetime import datetime


def get_last_modified_time(file_path):
    timestamp = os.path.getmtime(file_path)  # Отримуємо timestamp останньої модифікації
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Форматуємо в зручний вигляд



def get_file_size(file_path):
    return os.path.getsize(file_path)

def generate_directory_page(path, port, base_url="", ver="unknown"):
    file_list = os.listdir(path)
    directories = [f for f in file_list if os.path.isdir(os.path.join(path, f))]
    files = [f for f in file_list if os.path.isfile(os.path.join(path, f))]

    html_content = f"""
    <html>
    <head>
        <title>Index of {base_url}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                background-color: #f1f1f1;
                color: #333;
                margin: 20px;
            }}
            h1 {{
                font-size: 24px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 8px;
                text-align: left;
                border-bottom: 1px solid #ddd;
            }}
            tr:hover {{
                background-color: #f5f5f5;
            }}
            a {{
                text-decoration: none;
                color: #0000EE;
            }}
            a:visited {{
                color: #551A8B;
            }}
            hr {{
                border: 1px solid #ccc;
            }}
        </style>
    </head>
    <body>
        <h1>Index of {base_url}</h1>
        <table>
            <tr>
                <th>Name</th>
                <th>Size</th>
                <th>Last modified</th>
            </tr>
    """

    # Додаємо директорії
    for directory in directories:
        rel_path = os.path.join(base_url, directory).replace("\\", "/")
        html_content += f'''
            <tr>
                <td><a href="{rel_path}/">{directory}/</a></td>
                <td>-</td>
                <td>{get_last_modified_time(os.path.join(path, directory))}</td>
            </tr>
        '''

    # Додаємо файли
    for file in files:
        rel_path = os.path.join(base_url, file).replace("\\", "/")
        html_content += f'''
            <tr>
                <td><a href="{rel_path}">{file}</a></td>
                <td>{get_file_size(os.path.join(path, file))} bytes</td>
                <td>{get_last_modified_time(os.path.join(path, file))}</td>
            </tr>
        '''

    html_content += f"""
        </table>
        <hr>
        <p>CoretexWEB/{ver} - Running at port: {port}</p>
    </body>
    </html>
    """

    response = Response(html_content, content_type="text/html")
    response.headers["X-Powered-By"] = f"ATRCORE/Python"
    return response
