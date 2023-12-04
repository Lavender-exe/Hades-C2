import os
from configparser import ConfigParser
from config.colours import success, info

"""
TODO:
- Make it more malleable
    - UA for HTTP traffic
    - 
"""

profiles_obj = ConfigParser()

profiles_obj["DEFAULT"] = {
    "host_ip" : "127.0.0.1",
    "host_port" : "8443",
}

profiles_obj['current_profile'] = {
    "name" : "DEFAULT"
}

profiles_obj_path = 'config/config_files/profiles.ini'

def create_profile():
    if not os.path.exists(profiles_obj_path):
        with open(profiles_obj_path, 'w') as conf:
            profiles_obj.write(conf)
        success(f"Profiles config file '{profiles_obj_path}' created.")