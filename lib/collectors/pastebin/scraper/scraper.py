import json
import random
import time

import pika
import requests

import constants as lc
from utils.functions import *


class Scraper:
    count_fail = 0
    scraped_files = []

    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.channel()

        self.channel.queue_declare(
            queue=lc.DOWNLOADER_QUEUE,
            durable=True)

    def run(self):
        """
        This function is called by "main.py".
        It allows you to retrieve the metadata
        of the  files listed by the "pastebin.com" API.
        The metadata are sent to the queue "pastebin_downloader".
        """
        log_info('scrapper', 'run() started')
        scraping_url = f"{lc.SCRAPING_URL}?limit={lc.SCRAPING_LIMIT}"

        while 1:
            if self.count_fail > lc.MAX_FAILED_REQUEST:
                break

            if len(self.scraped_files) > lc.SCRAPING_LIMIT * 10:
                self.scraped_files = self.scraped_files[len(
                    self.scraped_files)//2:]

            r = requests.get(url=scraping_url)
            if r.status_code != 200:
                self.count_fail += 1
                msg = f"Error: GET:{scraping_url}, Status:{r.status_code}"
                log_warn('scrapper', msg)
                continue

            files_to_scrap = json.loads(r.text)
            files_to_scrap = sorted(files_to_scrap,
                                    key=lambda paste: paste['date'])

            for paste in files_to_scrap:
                if paste in self.scraped_files:
                    continue

                publish(
                    module='scraper',
                    channel=self.channel,
                    data=json.dumps(paste),
                    queue=lc.DOWNLOADER_QUEUE)

                self.scraped_files.append(paste)
            time.sleep(lc.SCRAPING_SLEEP + random.choice(lc.SCRAPING_DELAY))

        log_info('scraper', 'run() stopped')
