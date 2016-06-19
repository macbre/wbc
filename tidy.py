#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean the provided txt file before passing it to the indexer

./tidy.py issue.txt > clean.txt
"""
import fileinput
import sys


class TextTidy(object):
    def __init__(self, _in):
        self._in = _in

    def tidy(self, output=sys.stdout):
        buf = ''

        # do the stuff
        for line in self._in:
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
                if line == '':
                    continue

                line = "\n{}".format(line)

            # headings for subsequent pages in the same chapter - can be skipped
            if line.startswith('\x0c'):
                continue

            # merge consecutive lines that end with a line break (-)
            if line.endswith('-') and not line.endswith(' -'):
                buf += line[:-1]
            # merge lines that belong to a single sentence
            elif not line.endswith('.'):
                buf += line + ' '
            else:
                output.write((buf + line).rstrip() + "\n")
                buf = ''

        # print any remaining lines
        if buf != '':
            output.write(buf + "\n")


def main():
    tidy = TextTidy(fileinput.input())
    tidy.tidy(sys.stdout)

if __name__ == '__main__':
    main()
