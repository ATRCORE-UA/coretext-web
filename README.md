# Coretext-WEB - Web Server Project

Coretext-WEB is a web server that serves static files with SSL support and allows directory listing configuration through a JSON configuration file.

## Description

This project enables you to configure your own web server to serve static files over HTTPS with the option to enable/disable directory listing.


### Configuration File: `config.json`

```json
{
  "host": "0.0.0.0",  // Specifies the IP address or hostname where the server will listen for incoming requests.
  "port": 443,  // Specifies the port number where the server will listen for incoming connections.
  "enable_ssl": true,  // Enables SSL (Secure Sockets Layer) for secure communication over HTTPS.
  "ssl_cert": "Path/to/your/cert.pem",  // The path to your SSL certificate file (in .pem format).
  "ssl_key": "Path/to/your/key.pem",  // The path to the private key for your SSL certificate.
  "domain": "yourdomain.com",  // Your domain name (e.g., example.com) for the server.
  "ftp_srv_index": "true",  // Enables or disables directory listing. If "true", directories will be listed.
  "index_file": "index.html",  // The file that will be served when a directory is requested (e.g., index.html).
  "htdocs_path": "Path/to/your/htdocs", // Path to the 'htdocs' directory with your HTML files.
  "logs": "true" // Enable http request logs to access_log.txt.
  "py-scripts": true // Enables the web server to execute Python scripts as dynamic web pages.
  "ddos-protection": true // Enables DDOS-protection for a web-server.
}
```
### Default `config.json`

```json
{
  "host": "0.0.0.0",
  "port": 80,
  "enable_ssl": false,
  "ssl_cert": "Path/to/your/cert.pem",
  "ssl_key": "Path/to/your/key.pem",
  "domain": "yourdomain.com",
  "ftp_srv_index": "true",
  "index_file": "index.html",
  "htdocs_path": "Path/to/your/htdocs",
  "logs": "true",
  "py-scripts": true
  "ddos-protection": true
}
```
## DDOS-protection

### Configuration File: `ddos.json`

```json
{
    "max_requests": 150, // Number of allowed requests per minute.
    "block_time": 300 // The time for which the IP will be blocked.
}

```

### Default `ddos.json`

```json
{
    "max_requests": 100,
    "block_time": 300
}
```

## Commands

- `exit`/`stop` - stop the web server.
- `reload_conf` - reload server configuration (`config.json`).
- `ip_conf` - you can see your global IP adress.

```
==================================================
CoretexWEB/1.7.74S
Running at port: 80
Serving files from: C:/web-server/1.7.73A/htdocs
Python scripts execution: Enabled
SSL Enabled: No
==================================================
Enter command: ip_conf
Global: 34.123.231.45
Enter command:
```
Here you see `Enter command:` you can enter any command here.

## Setup
!Minimum Python 3.10 required!

### Step 1

Download latest ZIP of release from [here](https://github.com/ATRCORE-UA/coretext-web/releases/latest).

### Step 2

Unzip the ZIP to any location, e.g. `C:\coretext-web-x.x.xx`

### Step 3

Run `pip install -r requirements.txt` to install the required libraries.
If you encounter issues with dependencies, try running:
`pip install Flask`
`pip install Werkzeug`
`pip install requests`

### Step 4

Open [`config.json`](https://github.com/ATRCORE-UA/coretext-web/?tab=readme-ov-file#configuration-file-configjson) and configure it to your needs.

### Step 5 (final)

Run `python server.py` in the root directory.

## Now you have opensourse and simple web server✨!



## Supported .htaccess Rules:

- **Deny from all**  
  Denies access to all users.  
  **Response:** `403 Forbidden`.  
  **Example**:
`Deny from all`

- **Redirect**  
Redirects from one URL to another.  
**Response:** `301 Moved Permanently`.  
**Example**:
`Redirect /old-page /new-page`

- **ErrorDocument**  
Defines custom error pages for specific HTTP errors (e.g., 404).  
**Response:** Custom error page with specified status code.  
**Example**:
`ErrorDocument 404 /custom-404.html`

- **Options -Indexes**  
Disables directory listing.  
**Response:** `403 Forbidden with message "Directory listing is disabled".`  
**Example**:
`Options -Indexes`

- **ReturnStatus**  
Returns a custom HTTP status code.  
**Response:** The specified status code with no content.  
**Example**:
`ReturnStatus 418`

- **Redirecttourl**  
Returns a custom HTTP status code.  
**Response:** This file will take you to a specific URL.  
**Example**:
`Redirecttourl https://google.com/`

## .py web dynamic web-pages.

```
# web-page.py
print("<html><body><h1>Hello, World!</h1>")
print("<h1>This is CoretextWEB!</h1>")
```
### What does this mean to you?

- You can use `pip install mysql-connector-python` for connecting to MysqlDB's.
- You can use any python library to use in a python script to create a dynamic HTML page.
- It supports `Get-Requests` e.g. `http://localhost/get.py?data=yourdata`

- ### `!This functionality is available from CoretextWEB version 1.7.73A!`
