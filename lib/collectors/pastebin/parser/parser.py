import constants as lc
import utils.globals as gc
from review import Review
from utils.functions import *


class Parser:

    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue=lc.PARSER_QUEUE, durable=True)

    def run(self):
        """
        This function allows you to retrievethe information
        stored in the pastebin_parser queue.
        """
        log_info('parser', 'run() started')

        self.channel.basic_consume(
            queue=lc.PARSER_QUEUE,
            on_message_callback=Parser.callback)

        self.channel.start_consuming()

    def callback(ch, method, properties, body):
        """
        This function will be triggered when an element enter the  
        pastebin_parser queue. Review object will be create in
        order to parse the content of a text file stored
        at "tmp/pastebin/<filename>".
        """

        body = body.decode('utf-8')
        msg = f"Data {body} received from queue {lc.PARSER_QUEUE}"
        if gc.DEBUG:
            log_info('pastebin', msg)
        path = f"{lc.TEMP_STORAGE}/{body}"

        try:
            with open(path, 'r') as f:
                data = f.read()
        except Exception as e:
            msg = f"callback() failed, for file {body}: {e}"
            log_info('pastebin', msg)
            return

        delimiter = data.find('\n')
        metadata = data[0:delimiter]
        data = data[delimiter+1::]

        review = Review(metadata, data)
        review.search(path, body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
