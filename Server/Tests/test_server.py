import socket
import threading
import uuid

from Server.ServerOperation import LOCAL_HOST,PORT
from Server.Logger import Log

logger = Log(logger_name="test_server")

host = LOCAL_HOST
port = PORT

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

def mock_client(client_id):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            logger.info(f"Client {client_id}: Connecting to the server")
            client_socket.connect((host, port))
            logger.info(f"Client {client_id}: Connected to the server")

            # Example of sending data to the server
            message = f"Hello from client {client_id}"
            client_socket.sendall(message.encode('utf-8'))
            logger.info(f"Client {client_id}: Sent message to the server")

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
    simulate_clients(client_count=10)

