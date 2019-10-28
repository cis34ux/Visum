import os
import re
import shutil
from datetime import datetime

import pika

import constants as lc
import utils.globals as gc
from leak import Leak
from utils.functions import *

# Regex to extract email
REXEG_EMAIL = re.compile(
    r"(\b([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})\b)")
# Regex to extract leak
REGEX_LEAK = re.compile(
    r"(\b([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})([\|\:\;])([a-zA-Z0-9!\"#$%&'()*+,\-./:;<=>?@\[\]^_`{|}~]+)\b)")


def move(path, filename):
    """
    This function move a file from /tmp/collectors/pastebin/<filename>
    to /storage/collectors/pastebin/<date>/<hour>/<filename> .

    Returns:
        string: The path of the moved file
    """
    ts, key = filename.split('_')
    date = datetime.utcfromtimestamp(float(ts))

    folder = f"{lc.COMPRESSED_STORAGE}/{date.strftime('%Y-%m-%d')}"
    subfolder = f"{folder}/{date.strftime('%H')}"

    os.makedirs(folder, exist_ok=True)
    os.makedirs(subfolder, exist_ok=True)

    destination = f"{subfolder}/{key}"
    shutil.move(path, destination)
    return destination


class Review:
    leak = []

    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data

    def search(self, path, filename):
        self.leak = self.__search_leak__()

        if not self.leak:
            os.remove(path)
        else:
            l = Leak(self.metadata, self.leak)
            l.load()
            filename = move(path, filename)

    def __search_leak__(self):
        """
        This function extract from a file credentials
        using the regex REGEX_LEAK and return an array
        containing all extracted credentials.

        Returns:
            array: This array contains all extracted credentials
        """
        leaks = REGEX_LEAK.findall(self.data)
        results = []

        for element in leaks:
            line = element[0]
            email = REXEG_EMAIL.search(line)[0]
            password = line.replace(email, '')[1::]
            updated_line = email + ":" + password
            results.append(updated_line)
        return results