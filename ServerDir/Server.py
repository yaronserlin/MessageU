import socket
from threading import Thread

from Protocol import Protocol
from IO_Handler import read_port_from_file
from Logger import Log


class Server:
    PORT_FILENAME = "myport.info"
    LOCAL_HOST = "127.0.0.1"
    PORT = read_port_from_file(PORT_FILENAME)
    logger = Log(logger_name=__name__)

    @staticmethod
    def start_server():
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            host = Server.LOCAL_HOST
            port = Server.PORT

            server_socket.bind((host, port))
            server_socket.listen()

            Server.logger.info(f"Server listening on [{host}:{port}]")

            Server.run(server_socket)

            Server.logger.debug("Close server")
            server_socket.close()

        except Exception as e:
            Server.logger.error(e)

    @staticmethod
    def run(server_socket):
        while True:
            client_socket, address = server_socket.accept()
            Server.logger.info(f"Connection from [{address}]")

            # Server.logger.debug(f"client_socket: {client_socket}")
            Thread(target=Server.handle_client, args=(client_socket,)).start()

    @staticmethod
    def handle_client(client_socket):
        try:
            Server.logger.debug("Parse the request from socket")
            data = client_socket.recv(Protocol.HEADER_SIZE + Protocol.REGISTRATION_SIZE)
            parsed_request = Protocol.parse_request(data)

            Server.logger.info(f"Request with code [{parsed_request['header']['code']}] was successfully decrypted.")
            Server.logger.debug(f"Header: {parsed_request['header']}")
            Server.logger.debug(f"Payload: {parsed_request['payload']}")

        except ValueError as e:
            Server.logger.error(e)
        except Exception as e:
            Server.logger.error(e)

        client_socket.close()
