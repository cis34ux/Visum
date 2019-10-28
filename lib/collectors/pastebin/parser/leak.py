import hashlib
import json

import utils.globals as gc
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from utils.functions import *


class Leak:
    def __init__(self, metadata, data):
        self.metadata = metadata
        self.data = data

    def load(self, **kwargs):
        try:
            es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])
            success, _ = bulk(es, self.set_data(**kwargs),
                              request_timeout=60, raise_on_exception=False)

            msg = f"Datas inserted into elasticsearch: {success}"
            if gc.DEBUG:
                log_info('parser', msg)
            return True
        except Exception as e:
            msg = f"load() failed: {e}"
            log_warn('parser', msg)

    def set_data(self, index_name="leak", doc_type_name="credentials", source="pastebin"):
        for credentials in self.data:
            try:
                c = credentials.strip().split(":")
                mail = c[0].lower()
                password = c[1]
                if password:
                    primary_key = f"{mail}:{password}"
                    metadata = json.loads(self.metadata)
                    doc = self.prepare_data(mail, password)
                    yield {
                        "_index": index_name,
                        "_type": doc_type_name,
                        "_id": hashlib.sha256(primary_key.encode()).hexdigest(),
                        "source": source,
                        "metadata": metadata,
                        "data": doc
                    }
            except Exception as e:
                msg = f"set_leak() failed: {e}"
                log_warn('parser', msg)

    def prepare_data(self, mail, password):
        doc = {}
        doc["mail"] = mail
        doc["password"] = password
        doc["domain"] = mail.split('@')[-1]
        doc["length"] = len(password)
        doc["password_mask"] = get_mask(password)
        doc["contains_digits"] = check_digit(password)
        doc["contains_lower_case"] = check_lower(password)
        doc["contains_upper_case"] = check_upper(password)
        doc["contains_special"] = check_special(password)
        return doc
