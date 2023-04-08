import os
from Config.colours import *


def clear():
    os.system('cls||clear')


def help():
    """
    Shows the help menu
    :return:
    """

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
    clear / cls                       --> Clear Screen
""" + Style.RESET_ALL)

    # Seperator
    seperator()
    print("")
