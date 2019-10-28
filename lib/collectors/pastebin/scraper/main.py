import logging
from threading import Thread

import pika

import constants as lc
import utils.globals as gc
from scraper import Scraper
from utils.functions import *


def main():
    """
    This function allows you to initiate a connection
    to the rabbitmq server and then launch the scraper thread.
    """
    log_info('pastebin', 'scraper started')

    rabbit_params = pika.ConnectionParameters(
        host=gc.RABBITMQ_HOSTNAME,
        port=gc.RABBITMQ_PORT)

    connection = pika.BlockingConnection(rabbit_params)

    scraper = Scraper(connection)
    t = Thread(target=scraper.run)
    t.start()
    t.join()

    log_info('pastebin', 'scraper stopped')


if __name__ == '__main__':
    logging.basicConfig(filename=lc.LOGFILE, level=logging.INFO)
    main()
