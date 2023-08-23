from rich.style import Style
from rich.console import Console

console = Console(color_system="auto")
style = Style()

def success(function):
    console.print(f"[+] {function}", style="green")


def error(function):
    console.print(f"[!] {function}", style="red on white")


def info(function):
    console.print(f"[i] {function}", style="blue_violet")


def quit(function):
    console.print(f"[-] {function}", style="red")


def process(function):
    console.print(f"[*] {function}", style="yellow")


def seperator():
    console.print("".center(80, "="), style='medium_violet_red')
