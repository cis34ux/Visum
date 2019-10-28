import logging
import os
from threading import Thread

import pika

import constants as lc
import utils.globals as gc
from downloader import Downloader
from utils.functions import *


def main():
    """
    This function allows you to initiate a connection
    to the rabbitmq server and then launch the downloader thread.
    """
    log_info('pastebin', 'downloader started')
    os.makedirs(lc.TEMP_STORAGE, exist_ok=True)

    rabbit_params = pika.ConnectionParameters(
        host=gc.RABBITMQ_HOSTNAME,
        port=gc.RABBITMQ_PORT)

    connection = pika.BlockingConnection(rabbit_params)

    downloader = Downloader(connection)
    t = Thread(target=downloader.run)
    t.start()
    t.join()

    log_info('pastebin', 'downloader stopped')


if __name__ == '__main__':
    logging.basicConfig(filename=lc.LOGFILE, level=logging.INFO)
    main()
