import pyfiglet
from colorama import *
from config.commands import *
from config.config_create.create_profiles import create_profile
from modules.keygen import generate_certificate


def banner():
    clear()

    # Server Banner
    banner = pyfiglet.figlet_format("Hades", font="calgphy2", justify="center")
    console.print(f"[bold yellow]{banner}[/bold yellow]")
    
    console.print("By: Lavender-exe", style="medium_purple1")
    console.print("GNU General Public License v3.0", style="green")
    
    seperator()
    create_profile()

    if not os.path.exists('Generated Payloads'):
        process("Creating Generated Payloads Directory...")
        os.mkdir('Generated Payloads')
        success("Generated Payloads Directory Created")
        
    if not os.path.exists('certs'):
        process("Creating Certificates Directory...")
        os.mkdir('certs')
        success("certs Directory Created")
        
    if not os.path.exists('certs/key.pem'):
        generate_certificate()
    success("Config Complete")

    seperator()
    print("")

