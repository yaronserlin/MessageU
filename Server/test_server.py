import socket
import uuid

from Server import *
from IO_Handler import read_port_from_file
from Logger import Log

logger = Log(logger_name=__name__)

host = LOCAL_HOST
port = read_port_from_file(PORT_FILENAME)

def generate_unique_id():
    return uuid.uuid4()

def connect_and_execute(server_ip, server_port, user_id, action, *args):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            logger.debug(f"Connecting to the server for <{action.__name__}> (user: {user_id}, args: {args})")
            client_socket.connect((server_ip, server_port))
            return action(client_socket, user_id, *args)
        except Exception as e:
            logger.error(f"Server Error during {action}: {e}")
            return None

def mock_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            logger.debug(f"Connecting to the server")
            client_socket.connect((host, port))
        except Exception as e:
            logger.error(f"Server Error during connection: {e}")
            return None

if __name__ == "__main__":
    mock_client()
