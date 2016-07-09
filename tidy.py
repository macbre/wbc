#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean the provided txt file before passing it to the indexer

./tidy.py issue.txt > clean.txt
"""
from __future__ import unicode_literals, print_function

import fileinput
import logging
import sys
import re


class TextTidy(object):
    EMPTY_HEADING = '\x1f\x1d\x0b'
    PAGE_NUMBER = '\x0c'
    PAGE_BREAK = '\x1f\x1d'

    PAGE_NUMBER_RE = re.compile(r'^[\s\d]+$')

    def __init__(self, _in, chapter_break=''):
        self._in = _in
        self._logger = logging.getLogger(self.__class__.__name__)
        self._chapter_break = chapter_break

    def tidy(self, output=sys.stdout):
        buf = ''

        def _write(_line):
            output.write(_line + "\n")

        def _write_debug(_line):
            # output.write('##' + _line + "##\n")
            pass

        # do the stuff
        for line in self._in:
            try:
                line = line.decode('utf-8', 'ignore')
            except UnicodeDecodeError:
                self._logger.error('UTF-8 encoding error', exc_info=True)
                print(line)

            line = line.rstrip()

            _write_debug('#' + line + '#')

            # empty headings
            if line.startswith(self.EMPTY_HEADING):
                _write_debug('FOO_EMPTY_HEADING')
                pass
            # page numbers
            elif line.startswith(self.PAGE_NUMBER) and self.PAGE_NUMBER_RE.match(line):
                _write_debug('FOO_PAGE_NUMBER')
                continue
            # page breaks - headings
            elif line.startswith(self.PAGE_BREAK):
                line = line[2:]  # remove magic characters

                _write_debug('FOO_PAGE_BREAK')

                # ignore empty headings followed by the title
                if len(line) == 0:
                    continue

                line = "\n{}".format(line)

            # mark chapters (if they're written uppercase)
            if line.startswith('\x0c'):
                chapter = line[1:]

                if chapter.isupper():
                    _write_debug('FOO_CHAPTER')
                    line = self._chapter_break + line[1:]
                else:
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
