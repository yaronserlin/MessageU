import socket
from threading import Thread

from IO_Handler import read_port_from_file
from Logger import Log

PORT_FILENAME = "myport.info"
LOCAL_HOST = "127.0.0.1"
PORT = read_port_from_file(PORT_FILENAME)

logger = Log(logger_name=__name__)

def start_server():
    try:
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = LOCAL_HOST
        port = read_port_from_file(PORT_FILENAME)
        server_socket.bind((host,port))
        server_socket.listen()

        logger.info(f"Server listening on [{host}:{port}]")
        run(server_socket)
        logger.debug("Close server")
        server_socket.close()
    except Exception as e:
        logger.error(e)

def run(server_socket):

    while True:
        client_socket, address = server_socket.accept()
        logger.info(f"Connection from [{address}]")
        Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    logger.debug(f"Hello from handle_client! args: [{client_socket}]")

