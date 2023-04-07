from colorama import *
import sys
import pyfiglet
import os
from Config import colours

def banner():
    # Clear Screen
    os.system("cls||clear")

    # Add seperator
    colours.seperator()

    # Server Banner
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT)
    pyfiglet.print_figlet("Hades", font="calgphy2", justify="center")
    print(Style.RESET_ALL)

    # Credits
    print(Fore.LIGHTMAGENTA_EX + "By: Lavender-exe" + Style.RESET_ALL)
    print(Fore.LIGHTMAGENTA_EX + "GNU General Public License v3.0" + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX + '''
Credits: Joe Helle
https://ko-fi.com/s/0c3776a2a0
    ''' + Style.RESET_ALL)
    print(Fore.LIGHTRED_EX + "".center(80, "=") + Style.RESET_ALL)
    print("")

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

    Payload Commands
    ---------------------------------------------------------------------------------------

    winplant.py                       --> Windows Python Implant
    exeplant.py                       --> Windows Executable Implant
    linplant.py                       --> Linux Implant
    pshell_shell                      --> Powershell Implant

    Client Commands
    ---------------------------------------------------------------------------------------

    persist / pt                      --> Persist Payload (After Interacting with Session) 
    background / bg                   --> Background Session
    exit                              --> Kill Client Connection

    Misc Commands
    ---------------------------------------------------------------------------------------

    help / h                          --> Show Help Menu
""" + Style.RESET_ALL)

    # Seperator
    colours.seperator()
    print("")