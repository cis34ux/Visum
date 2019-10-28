import json

import constants as lc
import utils.globals as gc
from utils.functions import *


class Paste:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data

    def save(self):
        """
        This function allows you to write the metadata
        and the content of a paste into a file. Then the
        filename is sent to the rabbitmq queue "pastebin_parser".
        
        Returns:
            string: The filename of the created file
        """
        path = lc.TEMP_STORAGE
        metadata = json.loads(self.metadata)
        date, key = [metadata['date'], metadata['key']]
        filename = f"{date}_{key}.txt"
        try:
            with open(f'{path}/{filename}', 'a+') as f:
                f.write(f'{self.metadata.decode()}\n\n')
                f.write(self.data)
            if gc.DEBUG:
                log_info('downloader', '{} saved'.format(filename))
            return filename
        except Exception as e:
            msg = 'save() failed for {}, {}'.format(filename, e)
            log_warn('downloader', msg)
