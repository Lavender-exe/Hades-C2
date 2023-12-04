import os
from configparser import ConfigParser
from config.colours import success,info


config_obj = ConfigParser()
config_obj["DATABASE"] = {
    "targets_db" : "config/database/targets.db"
}

config_obj["SSL"] = {
    "certificate" : "certs/server.crt", 
    "privkey" : "certs/server.key",
}

config_obj["CERTIFICATE"] = {
    "country" : "US",
    "state" : "US",
    "locality" : "US",
    "org" : "dummycompany",
    "orgunit" : "dummyunit",
    "fqdn" : "localhost", # Change this
    "email" : "local@host.com",
}

# Create LOGGING File

config_file_path = 'config/config_files/server_config.ini'
def create_config():
    if not os.path.exists(config_file_path):
        # Write the configuration to the file
        with open(config_file_path, 'w') as conf:
            config_obj.write(conf)
        