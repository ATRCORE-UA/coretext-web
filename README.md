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
  "logs": "true"
}
```

## Commands

- `exit`/`stop` - stop the web server.
- `reload_conf` - reload server configuratiob (`config.json`)

```
==================================================
CoretexWEB/1.7.71B
Running at port: 80
Serving files from: C:\web-server\1.7.71B\htdocs
SSL Enabled: No
==================================================
Enter command:
```
Here you see `Enter command:` you can enter any command here.

## Setup
!Minimum python 3.10!
### Step 1

Download latest ZIP of release from [here](https://github.com/ATRCORE-UA/coretext-web/releases/latest).

### Step 2

Unzip the ZIP to any location, e.g. `C:\coretext-web-x.x.xx`

### Step 3

Run `pip install -r requirements.txt` to install the required libraries.

### Step 4

Open [`config.json`](https://github.com/ATRCORE-UA/coretext-web/?tab=readme-ov-file#configuration-file-configjson) and configure it to your needs.

### Step 5 (final)

Run `python server.py` in the root directory.

## Now you have opensourse and simple web server✨!


## .htaccess Rules Handler


### Supported .htaccess Rules:

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

