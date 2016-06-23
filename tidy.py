#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean the provided txt file before passing it to the indexer

./tidy.py issue.txt > clean.txt
"""
from __future__ import unicode_literals, print_function

import fileinput
import sys
import logging


class TextTidy(object):
    def __init__(self, _in):
        self._in = _in
        self._logger = logging.getLogger(self.__class__.__name__)

    def tidy(self, output=sys.stdout):
        buf = ''

        def _write(_line):
            output.write(_line + "\n")

        # do the stuff
        for line in self._in:
            try:
                line = line.decode('utf-8', 'ignore')
            except UnicodeDecodeError:
                self._logger.error('UTF-8 encoding error', exc_info=True)
                print(line)

            line = line.strip()

            # empty headings
            if line.startswith('\x1f\x1d\x0b'):
                pass
            # page numbers
            elif line.startswith('\x0c'):
                continue
            # page breaks - headings
            elif line.startswith('\x1f\x1d'):
                line = line[2:]  # remove magic characters

                # ignore empty headings followed by the title
                if len(line) == 0:
                    continue

                line = "\n{}".format(line)

            # headings for subsequent pages in the same chapter - can be skipped
            if line.startswith('\x0c'):
                continue

            # cleanup
            line = line.replace('\x1f', '')

            # merge consecutive lines that end with a line break (-)
            if line.endswith('-') and not line.endswith(' -'):
                buf += line[:-1]
            # merge lines that belong to a single sentence
            elif not line.endswith('.'):
                buf += line + ' '
            else:
                _write((buf + line).rstrip())
                buf = ''

        # print any remaining lines
        if buf != '':
            _write(buf)


def main():
    tidy = TextTidy(fileinput.input())
    tidy.tidy(sys.stdout)

if __name__ == '__main__':
    main()
