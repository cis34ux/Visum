import logging
import string
from datetime import datetime

import constants as lc
import pika
import utils.globals as gc


def log_info(log_type, message):
    """
    Args:
        log_type (string): the name of the module ex: pastebin
        message (string): the content of the message
    """
    logging.info(f"[ ]{datetime.now()}, {log_type}:	{message}")


def log_warn(log_type, message):
    logging.warning(f"[*]{datetime.now()}, {log_type}:	{message}")


def log_err(log_type, message):
    logging.error(f"[!]{datetime.now()}, {log_type}:	{message}")


def publish(module, channel, data, queue):
    """
    Publish in the queue <queue> a persistent message <data>
    which will be read by a consumer.
    """
    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=data,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                          ))
    msg = f"Data {data} sent to queue {queue}"
    if gc.DEBUG:
        log_info(module, msg)


def get_mask(s):
    """
    This function calculate the mask of a password
    which is equivalent to the password complexity.
    """
    mask = ""
    for c in s:
        if c.isdigit():
            mask += "?d"
        elif c.islower():
            mask += "?l"
        elif c.isupper():
            mask += "?u"
        else:
            mask += "?s"
    return mask


def check_special(s):
    for c in s:
        if c in string.punctuation or c.isspace():
            return True
    return False


def check_upper(s):
    return any(i.isupper() for i in s)


def check_lower(s):
    return any(i.islower() for i in s)


def check_digit(s):
    return any(i.isdigit() for i in s)
