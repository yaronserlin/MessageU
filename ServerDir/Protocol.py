import socket
import struct

import Logger

logger = Logger.Log(logger_name=__name__)


class Protocol:
    import struct

    # Constants for header and payload structure
    HEADER_FORMAT = "16s B H I"  # 16 bytes for ID, 1 byte for version, 2 bytes for code, 4 bytes for size
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # Calculate header size

    # Constants for request code 600 - Registration
    REGISTRATION_FORMAT = "255s 160s"  # 255 bytes for name, 160 bytes for public key
    REGISTRATION_SIZE = struct.calcsize(REGISTRATION_FORMAT)  # Calculate payload size for registration

    @staticmethod
    def parse_request(data):
        """
        Parses a binary request according to the described protocol.

        Args:
            data (bytes): The binary request data received.

        Returns:
            dict: Parsed request data including the header and payload.
        """
        if len(data) < Protocol.HEADER_SIZE:
            raise ValueError(f"Data size {len(data)} does not match the expected header size: {Protocol.HEADER_SIZE}.")

        # Parse the header
        header = struct.unpack(Protocol.HEADER_FORMAT, data[:Protocol.HEADER_SIZE])
        client_id = header[0]  # ID field (ignored by the server)
        version = header[1]
        code = header[2]
        payload_size = header[3]

        # Ensure payload size matches the remaining data
        if len(data) < Protocol.HEADER_SIZE + payload_size:
            raise ValueError(
                f"Data size {len(data)} does not match the expected payload size: {Protocol.HEADER_SIZE + payload_size}.")

        payload_data = data[Protocol.HEADER_SIZE:Protocol.HEADER_SIZE + payload_size]

        payload = Protocol._parse_payload(payload_data, code)

        return {
            "header": {
                "client_id": client_id,  # Ignored by server
                "version": version,
                "code": code,
                "payload_size": payload_size,
            },
            "payload": payload,
        }

    @staticmethod
    def _parse_payload(payload_data, code):

        # Parse payload based on the request code
        if code == 600:  # Registration request
            if len(payload_data) != Protocol.REGISTRATION_SIZE:
                raise ValueError(
                    f"Data size {len(payload_data)} does not match the expected for registration request: {Protocol.REGISTRATION_SIZE}.")
        elif code == 601: # User list request
            if len(payload_data) > 0:
                raise ValueError(
                    f"Data size {len(payload_data)} does not match the expected for user list request: {0}.")
            return None

            return Protocol._parse_registration_payload(payload_data)
        else:

            raise ValueError(f"Unsupported request code: {code}")

    @staticmethod
    def _parse_registration_payload(payload_data):
        """
        Parses the payload for a registration request (code 600).

        Args:
            payload_data (bytes): The payload data for the registration request.

        Returns:
            dict: Parsed payload data including the name and public key.
        """

        name_raw, public_key_raw = struct.unpack(Protocol.REGISTRATION_FORMAT,payload_data)
        # print(payload_data_raw)
        # payload_data_raw.rstrip(b'\x00')
        # name_raw, public_key_raw = struct.unpack(Protocol.REGISTRATION_FORMAT, payload_data)
        name = name_raw.rstrip(b'\x00').decode('ascii')  # Remove null bytes and decode
        public_key = public_key_raw.rstrip(b'\x00')  # Keep public key as bytes

        return {
            "name": name,
            "public_key": public_key,
        }

    # Example usage
    # data = receive_request_from_client()
    # parsed_request = parse_request(data)
    # print(parsed_request)

    # HEADER_FORMAT = "16s B H I"  # 16 bytes for ID, 1 byte for version, 2 bytes for code, 4 bytes for size
    # HEADER_SIZE = struct.calcsize(HEADER_FORMAT)
    #
    # NAME_FORMAT = "255s"
    # NAME_SIZE = struct.calcsize(NAME_FORMAT)
    #
    # PUBLIC_KEY_FORMAT = "160s"
    # PUBLIC_KEY_SIZE = struct.calcsize(PUBLIC_KEY_FORMAT)
    #
    # @staticmethod
    # def parse_header(data):
    #     if len(data) < Protocol.HEADER_SIZE:
    #         raise ValueError(f"Data size {len(data)} is insufficient for the expected header size {Protocol.HEADER_SIZE}.")
    #
    #     # Parse the header
    #     header = struct.unpack(Protocol.HEADER_FORMAT, data[:Protocol.HEADER_SIZE])
    #     client_id = header[0]
    #     version = header[1]
    #     code = header[2]
    #     payload_size = header[3]
    #
    #     return {
    #         "client_id": client_id,
    #         "version": version,
    #         "code": code,
    #         "payload_size": payload_size,
    #     }
    #
    # @staticmethod
    # def build_request(client_id, version, code, payload):
    #     if len(client_id) > 16:
    #         raise ValueError("Client ID must not exceed 16 bytes.")
    #
    #     client_id = client_id.ljust(16, '\x00')  # Pad with null bytes
    #     payload_size = len(payload)
    #
    #     # Pack the header
    #     header = struct.pack(Protocol.HEADER_FORMAT, client_id.encode('utf-8'), version, code, payload_size)
    #
    #     # Combine header and payload
    #     return header + payload
    #
    # @staticmethod
    # def parse_payload(data, code, size):
    #     if code == 600:
    #         payload_format = Protocol.NAME_FORMAT +" "+ Protocol.PUBLIC_KEY_FORMAT
    #         payload_size = Protocol.NAME_SIZE + Protocol.PUBLIC_KEY_SIZE
    #
    #         if size > payload_size:
    #             raise ValueError(f"Data size {size} is insufficient for the expected payload size {payload_size}.")
    #
    #         # if len(data) < payload_size:
    #         #     raise ValueError(f"Data size {len(data)} is insufficient for the expected payload size {payload_size}.")
    #
    #         payload = struct.unpack(payload_format,data[:size])
    #         name = payload[0].rstrip(b'\x00')
    #         public_key = payload[1].rstrip(b'\x00')
    #         return {
    #             "name": name,
    #             "public_key": public_key
    #         }
    #     elif code == 601:
    #         pass
    #     elif code == 602:
    #         pass
    #     elif code == 603:
    #         pass
    #
    #     logger.debug(f"code: {code}, data: {data}")


# # Example usage
# if __name__ == "__main__":
#     # Create a sample request
#     request = Protocol.build_request("Client123", 1, 200, b"Sample payload data")
#
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
#         client_socket.connect(("127.0.0.1", 1234))
#         client_socket.sendall(request)
#     # Parse the request
#     parsed_request = Protocol.parse_header(request)
#
#     print("Parsed Request:", parsed_request)
