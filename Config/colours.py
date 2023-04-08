from colorama import *


def success(function):
    print(Fore.GREEN + "[+] " + function + Style.RESET_ALL)


def error(function):
    print(Fore.RED + "[-] " + function + Style.RESET_ALL)


def info(function):
    print(Fore.BLUE + "[i] " + function + Style.RESET_ALL)


def quit(function):
    print(Fore.LIGHTRED_EX + "[+] " + function + Style.RESET_ALL)


def process(function):
    print(Fore.YELLOW + "[*] " + function + Style.RESET_ALL)


def seperator():
    print(Fore.LIGHTRED_EX + "".center(80, "=") + Style.RESET_ALL)
