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

for dump_url in sorted(dumps, reverse=True):
    print(dump_url)
    dump_html = index = requests.get('https://dumps.wikimedia.org/enwiki/' + dump_url).text
    soup_dump = BeautifulSoup(dump_html, 'html.parser')
    pages_xml = [a['href'] for a in soup_dump.find_all('a')
                 if a.has_attr('href') and a['href'].endswith('-pages-articles.xml.bz2')]
    if pages_xml:
        break
    time.sleep(0.8)

wikipedia_dump = pages_xml[0].rsplit('/')[-1]
url = 'https://dumps.wikimedia.org/' + pages_xml[0]
path = get_file(wikipedia_dump, url)
print(path)
