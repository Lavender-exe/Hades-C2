from colorama import *
import sys
import os

# Status Colours
def success(function):
    print (Fore.GREEN + "[+] " + function + Style.RESET_ALL)

def error(function):
    print (Fore.RED + "[-] " + function + Style.RESET_ALL)

def info(function):
    print (Fore.BLUE + "[i] " + function + Style.RESET_ALL)

# Server Colours

def quit(function):
    print (Fore.LIGHTRED_EX + function + Style.RESET_ALL)