from configparser import ConfigParser

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

config_obj["SERVER"] = {
    "host_ip" : "",
    "host_port" : "",
}

with open('config/config.ini', 'w') as conf:
    config_obj.write(conf)