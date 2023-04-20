from colorama import *
from time import sleep
import pyfiglet

from Config.commands import *


def banner():
    # Update Repo
    process("Updating Repository")
    os.system("git pull")
    sleep(1)

    # Clear Screen
    os.system("cls||clear")

    # Add seperator
    seperator()

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
    seperator()
    if not os.path.exists('Generated Payloads'):
        process("Creating Generated Payloads Directory...")
        os.mkdir('Generated Payloads')
        success("Generated Payloads Directory Created")
    seperator()
    print("")

