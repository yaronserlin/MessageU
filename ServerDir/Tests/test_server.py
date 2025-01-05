import random
import socket
import struct
import threading
import uuid

from pyexpat.errors import messages

from IO_Handler import read_port_from_file
from Server import Server
from Logger import Log

logger = Log(logger_name="test_server")

host = Server.LOCAL_HOST
port = read_port_from_file("../myport.info")


def generate_unique_id():
    return uuid.uuid4().bytes


def connect_and_execute(server_ip, server_port, user_id, action, *args):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            logger.debug(f"Connecting to the server for <{action.__name__}> (user: {user_id}, args: {args})")
            client_socket.connect((server_ip, server_port))
            return action(client_socket, user_id, *args)
        except Exception as e:
            logger.error(f"Server Error during {action}: {e}")
            return None

def build_register_request(client_id):
    payload = struct.pack("255s 160s", b"yaron serlin\0", b"123456789")
    header = struct.pack("16s B H I", b'', 1, 600, len(payload))
    return header + payload

def build_user_list_request(client_id):
    header = struct.pack("16s B H I", b'', 1, 601, 0)
    return header

def mock_client(client_id):
    rand = random.randint(0,1)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            logger.info(f"Client {client_id.hex()}: Connecting to the server")
            client_socket.connect((host, port))
            logger.info(f"Client {client_id.hex()}: Connected to the server")

            request = b""
            if rand == 0:
                request = build_register_request(client_id)
                logger.info(f"Send register request from client {client_id.hex()}")
            elif rand == 1:
                request = build_user_list_request(client_id)
                logger.info(f"Send user list request from client {client_id.hex()}")
            logger.debug(request)
            client_socket.sendall(request)
            logger.info(f"Client {client_id.hex()}: Sent message to the server")

            # Example of receiving data from the server
            # response = client_socket.recv(1024).decode('utf-8')
            # logger.info(f"Client {client_id}: Received response: {response}")
        except Exception as e:
            logger.error(f"Client {client_id}: Error during connection: {e}")


# Function to simulate multiple clients
def simulate_clients(client_count):
    threads = []
    for i in range(client_count):
        thread = threading.Thread(target=mock_client, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # simulate_clients(client_count=10)
    # client_id = generate_unique_id()
    # print(client_id)  # Binary 16-byte output
    # print(len(client_id))  # Should print 16
    # print(client_id.hex())  # Hexadecimal string representation

    mock_client(generate_unique_id())
