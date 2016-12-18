"""
Clean the provided txt file before passing it to the indexer

This entry point can be used for tests purposes

tidy issue.txt > clean.txt
"""
import fileinput
import sys

from wbc.tidy import TextTidy


def main():
    tidy = TextTidy(fileinput.input())
    tidy.tidy(sys.stdout)
