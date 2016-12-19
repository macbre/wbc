#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Imports Fair Use sources in DJVU  format from www.wbc.poznan.pl

Usage:
  fetch [--no-fetch] ID
  fetch (-h | --help)
  fetch --version

Arguments:
  ID            Publication ID

Options:
  -h --help     Show this screen.
  --version     Show version.
  --no-fetch    Don't fetch, generate index only.
"""
import json
from docopt import docopt
from wbc.fetch import WBCFetch


def main():
    """
    Execute WBCFetch with provided arguments
    """
    args = docopt(__doc__, version='WBC v0.1')

    wbc = WBCFetch(publication_id=int(args['ID']), no_fetch=args['--no-fetch'])

    # run the scraper and covert DJVU files to plain text
    wbc.run()

    # store issues index as JSON
    with open("%s/index.json" % wbc.get_path(), "w") as out:
        json.dump(wbc.get_json_index(), out, indent=2, separators=(',', ': '), sort_keys=True)

    # store issues index as HTML
    with open("%s/index.html" % wbc.get_path(), "w") as out:
        out.write(wbc.get_html_index().encode('utf8'))
