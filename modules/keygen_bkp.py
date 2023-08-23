import os
from config.colours import *
from configparser import ConfigParser

conf_obj = ConfigParser()
conf_obj.read('config/config.ini')
ssl_conf = conf_obj["SSL"]

# Generate RSA key 
def generate_rsa_key():
    os.system('openssl genrsa -out certs/server.key 2048')

# Generate Certificate Signing Request
def generate_csr():
    os.system(f'openssl req -new -key certs/server.key -out certs/signreq.csr -subj "/CN={ssl_conf["fqdn"]}"')

# Sign the certificate
def sign_cert():
    os.system('openssl x509 -req -days 365 -in certs/signreq.csr -signkey certs/server.key -out certs/server.crt')

# Verify the certificate
def verify_cert():
    os.system('openssl x509 -text -noout -in certs/certificate.pem')


def generate_certificate():
    process("Generating Private and Public Keys")
    generate_rsa_key()
    generate_csr()
    sign_cert()
    success("Done!")