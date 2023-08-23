import sqlite3
from rich.console import Console
from configparser import ConfigParser

config_obj = ConfigParser()
config_obj.read('config/config.ini')
database_config = config_obj["DATABASE"]

console = Console()

connect = sqlite3.connect(database_config["targets_db"])
# connect = sqlite3.connect(":memory:")
cursor = connect.cursor()

console.print("[bold yellow] [*] Creating Database")

cursor.execute("""CREATE TABLE IF NOT EXISTS 
targets(
    session integer primary key,
    status text,
    username text,
    privilege text,
    target text,
    operating_system text,
    check_in timestamp
)""")

console.print("[bold green] [+] Database Created")
connect.commit()
connect.close()