import logging
import os
from parser import Parser
from threading import Thread

import pika

import constants as lc
import utils.globals as gc
from utils.functions import *


def main():
    """
    This function allows you to initiate a connection
    to the rabbitmq server and then launch the parser thread.
    """
    log_info('pastebin', 'parser started')

    # Create directories if they do not exist
    for directory in [lc.TEMP_STORAGE, lc.COMPRESSED_STORAGE]:
        os.makedirs(directory, exist_ok=True)

    rabbit_params = pika.ConnectionParameters(
        host=gc.RABBITMQ_HOSTNAME,
        port=gc.RABBITMQ_PORT)

    connection = pika.BlockingConnection(rabbit_params)

    parser = Parser(connection)
    t = Thread(target=parser.run)
    t.start()
    t.join()

    log_info('pastebin', 'parser stopped')


if __name__ == '__main__':
    logging.basicConfig(filename=lc.LOGFILE, level=logging.INFO)
    main()
