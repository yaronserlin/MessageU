import re

from FileHandler import read_from_file
from Logger import Log

logger = Log(logger_name=__name__)
DEFAULT_PORT = 1357
port_4_digits_pattern = r"\d{4}"

def is_valid_port(port):
    return bool(re.fullmatch(port_4_digits_pattern, port))


def read_port_from_file(filename):
    port = read_from_file(filename)

    if not port:
        logger.warning(f"The file '{filename}' does not exist in the folder or empty.")
        logger.warning(f"Using the default port: {DEFAULT_PORT}")
        return DEFAULT_PORT

    if not is_valid_port(port):
        logger.error(f"The contents of the file '{filename}' do not match the port format - 4 digits.")
        logger.warning(f"Using the default port: {DEFAULT_PORT}")
        return DEFAULT_PORT

    logger.debug(f"Read from file '{filename}' port number: [{port}]")
    return int(port)




