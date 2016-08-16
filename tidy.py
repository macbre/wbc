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

        # do the stuff
        for i, line in enumerate(self._in):
            def _debug(msg):
                self._logger.debug('{} : [{}] ({} chars)'.format(i+1, msg, len(msg)))

            try:
                line = line.decode('utf-8', 'ignore')
            except UnicodeDecodeError:
                self._logger.error('UTF-8 encoding error', exc_info=True)
                print(line)

            line = line.rstrip()

            _debug(line)

            # empty headings
            if line.startswith(self.EMPTY_HEADING):
                _debug('FOO_EMPTY_HEADING')
                pass
            # page numbers
            elif (line.startswith(self.PAGE_NUMBER) or line.startswith(self.PAGE_BREAK)) \
                    and self.PAGE_NUMBER_RE.match(line.replace(self.PAGE_BREAK, '')):
                _debug('FOO_PAGE_NUMBER')
                continue
            # page breaks - headings
            elif line.startswith(self.PAGE_BREAK):
                line = line[2:]  # remove magic characters

                _debug('FOO_PAGE_BREAK')

                # ignore empty headings followed by the title (len == 0)
                # and chapters with a single character per line (len == 1)
                if len(line) < 2:
                    continue

                line = "\n{}".format(line)

            # mark chapters (if they're written uppercase)
            if line.startswith(self.PAGE_NUMBER):
                chapter = line[1:].lstrip()

                if chapter.isupper():
                    _debug('FOO_CHAPTER - [{}]'.format(chapter))

                    # ignore chapters with a single character per line (len == 1)
                    if len(chapter) > 1:
                        line = self._chapter_break + line[1:]
                    else:
                        line = self._chapter_break
                else:
                    continue

            # cleanup
            line = line.replace('\x1f', '')
            # _debug(line)

            # merge consecutive lines that end with a line break (-)
            if line.endswith('-') and not line.endswith(' -'):
                buf += line[:-1]
            # merge lines that belong to a single sentence
            elif not line.endswith('.'):
                buf += line + ' '
            else:
                _write((buf + line).replace(" \n", "\n").rstrip())
                buf = ''

        # print any remaining lines
        if buf != '':
            _write(buf)


def main():
    tidy = TextTidy(fileinput.input())
    tidy.tidy(sys.stdout)

if __name__ == '__main__':
    main()
