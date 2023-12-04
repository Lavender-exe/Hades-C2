import os
import configparser
import subprocess
import socket
from config.colours import *
from rich.table import Table
from rich import box
from time import sleep
from config.config_create.create_config_file import *
from config.config_create.create_profiles import *
from config.networking.communication import *
from modules.implant_conf.implant_gen import set_server_addr


profiles_config = profiles_obj["DEFAULT"]
database_config = config_obj["DATABASE"]
ssl_config = config_obj["SSL"]


def clear():
    subprocess.call('clear' if subprocess.Popen('clear', shell=True).wait() == 0 else 'cls', shell=True)


def update_repo():
    # Update Repo
    process("Updating Repository")
    os.system("git pull")
    sleep(1)
    success("Updated!")


def update_config(profile_name, host_ip, host_port):
    # Read existing configuration
    config = configparser.ConfigParser()
    config.read('config/config_files/profiles.ini')

    # Check if the profile exists
    if not config.has_section(profile_name):
        config.add_section(profile_name)

    # Update specific values for the given profile
    config.set(profile_name, 'host_ip', host_ip)
    config.set(profile_name, 'host_port', str(host_port))

    # Write the updated configuration back to the file
    with open('config/config_files/profiles.ini', 'w') as conf:
        config.write(conf)

    success(f"Config for {profile_name} Updated")


def switch_profile(profile_name):
    config = configparser.ConfigParser()
    config.read('config/config_files/profiles.ini')

    if profile_name in config:
        config['DEFAULT']['host_ip'] = config[profile_name].get('host_ip', 'default_ip')
        config['DEFAULT']['host_port'] = config[profile_name].get('host_port', 'default_port')

        config['current_profile'] = {'name': profile_name}

        with open('config/config_files/profiles.ini', 'w') as conf:
            config.write(conf)

        success(f"Using configuration from profile: {profile_name}")
    else:
        error(f"Profile '{profile_name}' does not exist. Using default configuration.")
    
    
def create_profile(profile_name, host_ip, host_port):
    config = configparser.ConfigParser()
    config.read('config/config_files/profiles.ini')

    # Check if the profile already exists
    if profile_name in config:
        print(f"Profile '{profile_name}' already exists.")
        return

    # Create the profile section
    config[profile_name] = {
        'host_ip': host_ip,
        'host_port': str(host_port),
    }

    # Write the updated configuration back to the file
    with open('config/config_files/profiles.ini', 'w') as conf:
        config.write(conf)

    success(f"Profile '{profile_name}' created with host_ip={host_ip} and host_port={host_port}")


def get_current_profile():
    # Read existing configuration
    config = configparser.ConfigParser()
    config.read('config/config_files/profiles.ini')

    # Check if a profile is currently set
    if 'current_profile' in config:
        current_profile = config['current_profile']['name']
        host_ip = config[current_profile].get('host_ip', 'default_ip')
        host_port = int(config[current_profile].get('host_port', 'default_port'))

        print(f"Current Profile: {current_profile}")
        print(f"Host IP: {host_ip}")
        print(f"Host Port: {host_port}")
    else:
        print("No profile is currently set.")


def list_profiles():
    profiles_config = ConfigParser()
    profiles_config.read('config/config_files/profiles.ini')

    profiles = [section for section in profiles_config.sections() if section != "current_profile"]

    if profiles:
        print("Available Profiles:")
        for profile in profiles:
            print(f"- {profile}")
    else:
        print("No profiles found.")
        

def start_web_server():
    global web_server, web_servers
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(ssl_config["certificate"])
    handler = http.server.SimpleHTTPRequestHandler
    address = ((web_server_ip, int(web_server_port)))
    devnull = open(os.devnull, 'w')
    # sys.stdout = devnull
    sys.stderr = devnull
    with socketserver.TCPServer(address, handler) as web_server:
        web_server.socket = context.wrap_socket(web_server.socket, server_side=True)
        web_server.serve_forever()
    # web_server = socketserver.TCPServer(address, handler)
    # web_server.serve_forever()

    
def stop_web_server():
    global web_server, web_servers
    if web_server:
        web_server.shutdown()
        web_server.server_close()
        web_server = None
    for server in web_servers:
        server[2] = 'Dead'
    print('[+] Web server stopped.')


def help_menu():
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
    help_table.add_row("", "listeners", "-g | generate", "", "Generate Listener")
    help_table.add_row("", "listeners", "-l | list", "", "List Listeners")
    
    help_table.add_row("Session Commands", "", "", "", "")
    help_table.add_row("", "sessions", "-l | list", "", "List Active/Dead Sessions")
    help_table.add_row("", "sessions", "-i | interact", "NUM", "Interact with Session")
    help_table.add_row("", "sessions", "-k | kill", "NUM", "Kill Active Session")
    
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
    
    help_table.add_row("Profile Commands", "", "", "", "")
    help_table.add_row("", "profile", "update", "", "Update Config File")
    help_table.add_row("", "profile", "current", "", "View Current Profile")
    help_table.add_row("", "profile", "list", "", "View All Profiles")
    help_table.add_row("", "profile", "create", "", "Create Config Profile")
    help_table.add_row("", "profile", "switch", "", "Switch to a different Profile")
    
    console.print(help_table)