#!/usr/bin/python  
# Configures an HTTPS server to deliver directory contents.  
import sys  
import ssl  
from rich.console import Console
console = Console()

listener = ('localhost', 443)  # https://localhost:443/  
certificate_fl = 'server.crt'
privatekey_fl = 'server.key'
# Python version 3.  
if sys.version_info[0] == 3:  
    import http.server  
    httpd = http.server.HTTPServer(listener, http.server.SimpleHTTPRequestHandler)  
# Python 2 version  
elif sys.version_info[0] == 2:  
    import BaseHTTPServer, SimpleHTTPServer  
    httpd = BaseHTTPServer.HTTPServer(listener, SimpleHTTPServer.SimpleHTTPRequestHandler)  
# Wrap the socket with SSL  
httpd.socket = ssl.wrap_socket(httpd.socket,  
                certfile=certificate_fl, keyfile=privatekey_fl, server_side=True)  
# Start listening  
console.print("[bright blue]\nHosting on: https://localhost:443/")
httpd.serve_forever()  