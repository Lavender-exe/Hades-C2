from OpenSSL import crypto, SSL
from time import gmtime, mktime
from configparser import ConfigParser
from rich.console import Console

console = Console()
conf_obj = ConfigParser()

conf_obj.read('config/config.ini')
ssl_conf = conf_obj["SSL"]
cert_conf = conf_obj["CERTIFICATE"]

def generate_certificate(
    emailAddress=cert_conf["email"],
    commonName=cert_conf["fqdn"],
    countryName=cert_conf["country"],
    localityName=cert_conf["locality"],
    stateOrProvinceName=cert_conf["state"],
    organizationName=cert_conf["org"],
    organizationUnitName=cert_conf["orgunit"],
    serialNumber=0,
    validityStartInSeconds=0,
    validityEndInSeconds=10*365*24*60*60,
    KEY_FILE = ssl_conf["privkey"],
    CERT_FILE= ssl_conf["certificate"]):

    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    cert = crypto.X509()
    cert.get_subject().C = countryName
    cert.get_subject().ST = stateOrProvinceName
    cert.get_subject().L = localityName
    cert.get_subject().O = organizationName
    cert.get_subject().OU = organizationUnitName
    cert.get_subject().CN = commonName
    cert.get_subject().emailAddress = emailAddress
    cert.set_serial_number(serialNumber)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(validityEndInSeconds)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha512')
    with open(CERT_FILE, "wt") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
    with open(KEY_FILE, "wt") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

console.print("[bold yellow] [*]Generating Certificate")
generate_certificate()
console.print("[bold green] [+]Certificate Generated")