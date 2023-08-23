import os
from config.colours import *
from rich.table import Table
from rich import box
from time import sleep
from config.create_config_file import *

def clear():
    os.system('cls||clear')


def update_repo():
    # Update Repo
    process("Updating Repository")
    os.system("git pull")
    sleep(1)
    success("Updated!")
    

def help():
    """
    Shows the help menu
    :return:
    """
    help_table = Table(title="Help Menu",
                        box=box.ROUNDED)
    
    help_table.add_column("Module", justify="center", style="bold blue")
    help_table.add_column("Command", justify="center", style="bold violet")
    help_table.add_column("Command Prefix", justify="left", style="bold white")
    help_table.add_column("Command Argument", justify="center", style="bold violet")
    help_table.add_column("Description", justify="right", style="bold blue")
    
    help_table.add_row("Listener Commands", "", "", "", "")
    help_table.add_row("", "listeners", "-g | --generate", "", "Generate Listener")
    
    help_table.add_row("Session Commands", "", "", "", "")
    help_table.add_row("", "sessions", "-l | --list", "", "List Active/Dead Sessions")
    help_table.add_row("", "sessions", "-i | --interact", "NUM", "Interact with Session")
    help_table.add_row("", "sessions", "-k | --kill", "NUM", "Kill Active Session")
    
    help_table.add_row("Payload Commands", "", "", "", "")
    help_table.add_row("", "winpy", "", "", "Generate Windows Python Implant")
    help_table.add_row("", "exepy", "", "", "Generate Executable Python Implant")
    help_table.add_row("", "linpy", "", "", "Generate Linux Python Implant")
    help_table.add_row("", "pshell_shell", "", "", "Generate PowerShell Cradle")
    
    help_table.add_row("Client Commands", "", "", "", "")
    help_table.add_row("", "persist | pt", "", "", "Add Persistence Method")
    help_table.add_row("", "background | bg", "", "", "Background Session")
    help_table.add_row("", "exit", "", "", "Kill Current Session")
    
    help_table.add_row("Server Commands", "", "", "", "")
    help_table.add_row("", "help | h", "", "", "Display This Menu")
    help_table.add_row("", "clear | cls", "", "", "Clear Screen")
    help_table.add_row("", "update", "repo", "", "Update Repository")
    help_table.add_row("", "update", "config", "", "Update Config File")
    
    console.print(help_table)