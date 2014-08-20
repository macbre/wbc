#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Imports Fair Use sources in DJVU  format from www.wbc.poznan.pl

Usage:
  fetch.py [--no-fetch] ID
  fetch.py (-h | --help)
  fetch.py --version

Arguments:
  ID            Publication ID

Options:
  -h --help     Show this screen.
  --version     Show version.
  --no-fetch    Don't fetch, generate index only.
"""

import json
import logging
import os
import re
import subprocess
import tempfile

from docopt import docopt
from lxml import html
import requests

logging.basicConfig(level=logging.DEBUG)


class WBCError(Exception):
    pass


class WBCFetch(object):
    def __init__(self, publication_id, no_fetch=False):
        self.publication_id = publication_id
        self.index_url = "http://www.wbc.poznan.pl/dlibra/publication?id=%d&tab=1" % self.publication_id

        self.no_fetch = no_fetch

        self.path = "publications/%d" % self.publication_id

        self.logger = logging.getLogger("wbc")
        self.session = requests.Session()

        self.logger.debug("Index URL: %s", self.index_url)

        self.index = {
            "index": self.index_url,
            "name": '',
            "copyrights": '',
            "years": [],
            "issues": [],
            "count": 0
        }

        # przygotuj strukturę katalogów
        self.make_dir("/issues")

    def get_path(self):
        return self.path

    def get_index(self):
        return self.index

    def get_publication_id(self):
        return self.publication_id

    def make_dir(self, suffix):
        try:
            os.makedirs(self.get_path() + "/" + suffix)
        except OSError:
            pass

    def run(self):
        r = self.session.get(self.index_url)

        if r.status_code != 200:
            raise WBCError("HTTP request failed!")

        tree = html.fromstring(r.text)

        name = tree.xpath('//h2')[0].text.strip()
        copyrights = tree.xpath('//a[contains(@href, "671_1")]')[0].text
        items = tree.xpath('//div[@id="struct"]/ul//ul/li/a[@class="item-content"]')

        self.logger.debug("%s (%s)", name, copyrights)
        self.logger.debug("Got %d year(s) of issues", len(items))

        self.index['name'] = name
        self.index['copyrights'] = copyrights

        # roczniki (od najstarszych)
        years = []

        for item in reversed(items):
            year = item.text.strip()
            url = item.attrib.get('href')

            year = re.sub('[^0-9]', '_', year)

            self.index['years'].append({
                "year": year,
                "index": url
            })

            years.append((year, url))

        # numery
        for year, url in years:
            self.logger.debug("Year %s: <%s>", year, url)

            # przygotuj strukturę katalogów
            self.make_dir("/issues/" + year)

            r = self.session.get(url)
            tree = html.fromstring(r.text)

            # linki do <http://www.wbc.poznan.pl/dlibra/editions-content?id=129941>
            items = tree.xpath('//a[@class="contentTriggerStruct"]')

            self.index['count'] += len(items)

            for item in reversed(items):
                name = item.attrib.get('title', '').strip(' -')
                url = item.attrib.get('href')

                # pobierz ID pliku dla danego numeru
                r = self.session.get(url)
                issue_id = int(re.search('content_url=/Content/(\d+)/index.djvu', r.text).group(1))

                djvu = "http://www.wbc.poznan.pl/Content/%d/index.djvu" % issue_id
                zip = "http://www.wbc.poznan.pl/Content/%d/zip/" % issue_id

                self.logger.debug("%s: <%s>", name, djvu)

                self.index['years'].append({
                    "year": year,
                    "name": name,
                    "id": issue_id,
                    "djvu": djvu,
                    "zip": zip,
                })

                # --no-fetch
                if self.no_fetch is True:
                    continue

                # pobierz archiwum, rozpakuj i wygeneruj plik txt z treścią
                tmp_dir = tempfile.mkdtemp(prefix="wbc")
                cmd = ['./djvuzip2txt.sh', zip, tmp_dir]

                self.logger.debug("cmd: %s", cmd)

                # @see https://docs.python.org/2/library/subprocess.html#subprocess.call
                with open("%s/issues/%s/%d.txt" % (self.get_path(), year, issue_id), "wb") as f:
                    self.logger.debug("Output: %s", f.name)

                    proc = subprocess.Popen(cmd, stdout=f)
                    proc.wait()

                    f.flush()

                    if proc.returncode != 0:
                        raise Exception("Command failed!")

if __name__ == '__main__':
    arguments = docopt(__doc__, version='WBC v0.1')

    wbc = WBCFetch(publication_id=int(arguments['ID']), no_fetch=arguments['--no-fetch'])

    # zapisz indeks publikacji do pliku JSON
    wbc.run()

    with open("%s/index.json" % wbc.get_path(), "w") as out:
        json.dump(wbc.get_index(), out, indent=2, separators=(',', ': '), sort_keys=True)
