#!/usr/bin/python  
# Configures an HTTPS server to deliver directory contents.  
import sys  
import ssl  
from rich.console import Console
console = Console()

listener = ('localhost', 443)  # https://localhost:443/  
certificate_fl = 'server.crt'
privatekey_fl = 'server.key'
sslSettings = ssl.SSLContext()


if sys.version_info[0] == 3:  
    import http.server  
    httpd = http.server.HTTPServer(listener, http.server.SimpleHTTPRequestHandler)  

elif sys.version_info[0] == 2:  
    import BaseHTTPServer, SimpleHTTPServer  
    httpd = BaseHTTPServer.HTTPServer(listener, SimpleHTTPServer.SimpleHTTPRequestHandler)  


sslSettings.load_cert_chain(certfile=certificate_fl, keyfile=privatekey_fl)
httpd.socket = sslSettings.wrap_socket(httpd.socket, server_side=True)  


console.print("[bright blue]\nHosting on: https://localhost:443/")
httpd.serve_forever()  