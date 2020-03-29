import requests
from bs4 import BeautifulSoup
import os
import time
from keras.utils import get_file
from urllib.request import urlretrieve
import xml.sax
import subprocess
import re
import mwparserfromhell
import json

index = requests.get("https://dumps.wikimedia.org/enwiki/").text

soup_index = BeautifulSoup(index, "html.parser")

dumps = [a["href"] for a in soup_index.find_all("a") if a.has_attr("href") and a.text[:-1].isdigit()]
pages_xml = 0
for dump_url in sorted(dumps, reverse=True):
    print(dump_url)
    dump_html = index = requests.get('https://dumps.wikimedia.org/enwiki/' + dump_url).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')
    pages_xml = [a['href'] for a in soup_dump.find_all('a')
                 if a.has_attr('href') and a['href'].endswith('-pages-articles.xml.bz2')]
    if pages_xml:
        break
    time.sleep(0.8)


# wikipedia_dump = pages_xml[0].rsplit('/')[-1]
# url = 'https://dumps.wikimedia.org/' + pages_xml[0]
# path = get_file(wikipedia_dump, url)
# print(path)


def process_article(title, text):
    rotten = [(re.findall('\d\d?\d?%', p), re.findall('\d\.\d\/\d+|$', p), p.lower().find('rotten tomatoes')) for p in
              text.split('\n\n')]
    rating = next(((perc[0], rating[0]) for perc, rating, idx in rotten if len(perc) == 1 and idx > -1), (None, None))
    wikicode = mwparserfromhell.parse(text)
    film = next((template for template in wikicode.filter_templates()
                 if template.name.strip().lower() == 'infobox film'), None)
    if film:
        properties = {param.name.strip_code().strip(): param.value.strip_code().strip()
                      for param in film.params
                      if param.value.strip_code().strip()
                      }
        links = [x.title.strip_code().strip() for x in wikicode.filter_wikilinks()]
        return (title, properties, links) + rating


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._movies = []
        self._current_tag = None

    def characters(self, content):
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        if name in ("title", "text"):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        if name == self._current_tag:
            self._values[name] = " ".join(self._buffer)

        if name == "page":
            movie = process_article(**self._values)
            if movie:
                self._movies.append(movie)


# parser = xml.sax.make_parser()
# handler = WikiXmlHandler()
# parser.setContentHandler(handler)
# for line in subprocess.Popen(['bzcat'], stdin=open(path), stdout=subprocess.PIPE).stdout:
#     try:
#         parser.feed(line)
#     except StopIteration:
#         break
#
# with open('generated/wp_movies.ndjson', 'wt') as fout:
#     for movie in handler._movies:
#         fout.write(json.dumps(movie) + '\n')


with open('data/wp_movies_10k.ndjson') as fin:
    movies = [json.loads(l) for l in fin]
   