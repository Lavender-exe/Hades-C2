from modules.implant_conf.implant_gen import make_exe, make_file
from config.colours import success, error, info, process

def winpy():
    """
    Generates a Python implant for Windows
    :return:
    """
    make_file("winpy.py")

# Linux Payloads
def linpy():
    """
    Generates a Python implant for Linux
    :return:
    """
    make_file("linpy.py")

# EXE Payloads
def exepy():
    """
    EXE Payload Generator
    :return:
    """
    make_exe("winpy.py")