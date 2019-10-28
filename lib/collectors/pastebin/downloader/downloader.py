import json
import random
import time

import pika
import requests

import constants as lc
import utils.globals as gc
from paste import Paste
from utils.functions import *


class Downloader:

    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.channel()

        for queue in [lc.DOWNLOADER_QUEUE, lc.PARSER_QUEUE]:
            self.channel.queue_declare(queue=queue, durable=True)

    def run(self):
        """
        This function allows you to retrievethe information
        stored in the pastebin_downloader queue.
        """
        log_info('downloader', 'run() started')

        self.channel.basic_consume(
            queue=lc.DOWNLOADER_QUEUE,
            on_message_callback=Downloader.callback)

        self.channel.start_consuming()

    def callback(ch, method, properties, body):
        """
        This function will be triggered when an element enter the  
        pastebin_downloader queue. Paste object will be create in
        order to save the content of the Paste in a text file stored
        at "tmp/pastebin/<filename>".
        Then the filename is sent to the queue "pastebin_parser".
        """
        msg = f"Data {body} received from queue {lc.DOWNLOADER_QUEUE}"
        if gc.DEBUG:
            log_info('downloader', msg)

        time.sleep(lc.DOWNLOADING_SLEEP + random.choice(lc.DOWNLOADING_DELAY))

        scrape_url = json.loads(body)['scrape_url']
        r = requests.get(url=scrape_url)
        if r.status_code != 200:
            msg = f"Connection error: GET:{scrape_url}, Status:{r.status_code}"
            log_info('downloader', msg)
            return

        file = Paste(
            metadata=body,
            data=r.text)

        filename = file.save()
        ch.basic_ack(delivery_tag=method.delivery_tag)

        publish(
            module='downloader',
            channel=ch,
            data=filename,
            queue=lc.PARSER_QUEUE)
