from  Logger import Log
from  FileHandler import *
from IO_Handler import read_port_from_file
from Server import start_server


def main():
    logger = Log(logger_name=__name__)
    start_server()

if __name__ == '__main__':
    main()