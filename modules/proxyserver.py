import socket
import threading
import sys
import base64
def client_handler(client_socket):
    try:
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        comm_thread = threading.Thread(target=comm_out, args=(client_socket, remote_socket))
        comm_thread.start()
        while True:
            data = remote_socket.recv(8192)
            # intrans_message_capture = data.decode()
            # print(intrans_message_capture)
            # decoded_intrans_message_capture = base64.b64decode(intrans_message_capture).decode()
            # print(decoded_intrans_message_capture)
            if len(data) == 0:
                break
            client_socket.send(data)

    except ConnectionAbortedError:
        print(f"Connection terminated by {client_socket[0]}")
        pass

    except Exception as e:
        print(f"An error occurred: {e}")
        pass

    finally:
        client_socket.close()
        remote_socket.close()

def comm_out(client_socket, remote_socket):
    while True:
        data = client_socket.recv(8192)
        # intrans_message_capture = data.decode()
        # print(intrans_message_capture)
        # decoded_intrans_message_capture = base64.b64decode(intrans_message_capture).decode()
        # print(decoded_intrans_message_capture)
        if len(data) == 0:
            break
        remote_socket.send(data)

def start_proxy_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((sys.argv[3], int(sys.argv[4])))
    server_socket.listen()
    print(f'Proxy server is listening on port {sys.argv[4]}...')

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address[0]}:{client_address[1]}')
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

# Error handling for incorrect syntax
if len(sys.argv) < 3:
    print("Usage: python proxy_server.py <remote_server> <remote_port> <server_ip> <server_port>")
    sys.exit(0)

remote_host = sys.argv[1]
remote_port = int(sys.argv[2])

try:
    start_proxy_server()

except KeyboardInterrupt:
    user_input = input("Proxy server interrupted. Do you want to terminate? (y/n): ")
    if user_input.lower() == 'y':
        print("Terminating the proxy server...")
        sys.exit(0)
