#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clean the provided txt file before passing it to the indexer

./tidy.py issue.txt > clean.txt
"""
import fileinput

buf = ''


# do the stuff
for line in fileinput.input():
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
        print (buf + line).rstrip()
        buf = ''

# print any remaining lines
if buf != '':
    print buf
