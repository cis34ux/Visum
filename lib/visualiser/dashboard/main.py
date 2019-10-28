import logging
import os

import requests

from elasticsearch import Elasticsearch
from flask import Flask, render_template, request

app = Flask(__name__)

es = Elasticsearch(['http://elastic:changeme@elasticsearch:9200'])

logging.basicConfig(
    filename=f"log/dashboard_{os.getenv('HOSTNAME')}.log", level=logging.INFO)


def is_up(url):
    """
    This function check if
    a server is reachable.
    """
    try:
        r = requests.get(url=url)
        if r.status_code != 200:
            return False
        return True
    except:
        return False


def get_count(index, doc_type, source):
    """
    This function count the number of hits
    for a specific index, doc_type and source.
    """
    try:
        extract = es.count(index=index, doc_type=doc_type, body={
                           "query": {"match": {"source": source}}})
        return extract
    except:
        return {}


@app.route("/")
def index():
    sources = {"pastebin": {"url": "https://scrape.pastebin.com/api_scraping.php", "is_up": None,
                            "logo": None}, "github": {"url": "https://api.github.com/", "is_up": None, "logo": None}}
    for source in sources:
        sources[source]["is_up"] = is_up(sources[source]['url'])
        sources[source]["logo"] = f"static/img/logos/{source}.png"
    return render_template("index.html", sources=sources)


@app.route("/leaks", methods=['GET', 'POST'])
def leaks():
    if request.method != 'POST':
        counts = {}
        for doc_type in ["credentials", "mails"]:
            for source in ["pastebin"]:
                try:
                    counts[doc_type] = {source: get_count(
                        'leak', doc_type, source)["count"]}
                except:
                    counts[doc_type] = {source: "Error"}
        return render_template("leaks.html", counts=counts)
    query_data = request.form.get('query_data')
    query_type = request.form.get('query_type')
    return render_template("leaks.html", query=[query_data, query_type])


@app.route("/dorks")
def dorks():
    return render_template("dorks.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
