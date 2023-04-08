from colorama import *
from time import sleep
import pyfiglet
import os
from Config import colours


def banner():
    # Update Repo
    colours.process("Updating Repository")
    os.system("git pull")
    sleep(1)

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

