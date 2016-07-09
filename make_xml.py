#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generates SphinxSE-compatible XML stream with documents from a given publication / set of publications

XML can then be used to index publication using SphinxSE xmlpipe2 feature

Usage:
  make_xml.py ID
  make_xml.py (-h | --help)
  make_xml.py --version

Arguments:
  ID            Publication ID (can be comma-separated list of IDs)

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import logging
import json

from io import StringIO
from sys import stdout
from xml.sax.saxutils import XMLGenerator

from docopt import docopt

from tidy import TextTidy

logging.basicConfig(level=logging.DEBUG)


class SphinxXML(object):

    TAG_ROOT = 'sphinx:docset'
    TAG_SCHEMA = 'sphinx:schema'
    TAG_DOCUMENT = 'sphinx:document'

    def __init__(self, output=stdout):
        self._generator = XMLGenerator(encoding='utf-8', out=output)
        self._output = output

        self._logger = logging.getLogger(self.__class__.__name__)

        self._schema = {
            'field': [],
            'attr': []
        }
        self._document_id = 0

    def add_field(self, name):
        self._schema['field'].append({
            "name": name
        })

    def add_attr(self, name, attr_type, **kwargs):
        attr = kwargs
        attr['name'] = name
        attr['type'] = attr_type

        self._schema['attr'].append(attr)

    def start(self):
        self._generator.startDocument()
        self._generator.startElement(self.TAG_ROOT, {})

        # print schema
        self._generator.ignorableWhitespace("\n\n")
        self._generator.startElement(self.TAG_SCHEMA, {})

        for key, items in self._schema.items():
            for item in items:
                self._generator.ignorableWhitespace("\n\t")
                self._generator.startElement('sphinx:{}'.format(key), attrs=item)
                self._generator.endElement('sphinx:{}'.format(key))

        self._generator.ignorableWhitespace("\n")
        self._generator.endElement(self.TAG_SCHEMA)
        self._generator.ignorableWhitespace("\n\n")
        self._output.flush()

    def add_document(self, **kwargs):
        # auto-generate incrementing document IDs
        self._document_id += 1

        self._logger.info('Adding document #{}'.format(self._document_id))
        self._generator.startElement(self.TAG_DOCUMENT, {"id": str(self._document_id)})

        try:
            for key, val in kwargs.items():
                self._generator.ignorableWhitespace("\n\t")
                self._generator.startElement(key, {})
                self._generator.characters(val)
                self._generator.endElement(key)
        except ValueError:
            self._logger.error('add_document failed (doc ID #{})'.format(self._document_id), exc_info=True)

        self._generator.ignorableWhitespace("\n")
        self._generator.endElement(self.TAG_DOCUMENT)
        self._generator.ignorableWhitespace("\n\n")
        self._output.flush()

    def end(self):
        self._generator.endElement(self.TAG_ROOT)
        self._generator.endDocument()

        self._logger.info('XML closed')


def get_content_stream(publication_id, issue_year, issue_id, chapter_break=''):
    """
    :type publication_id int
    :type issue_id int
    :type issue_year int
    :type chapter_break str
    :rtype StringIO
    """
    file_path = 'publications/{}/issues/{}/{}.txt'.format(publication_id, issue_year, issue_id)

    output = StringIO()

    with open(file_path, mode='rb') as fp:
        TextTidy(_in=fp, chapter_break=chapter_break).tidy(output=output)

    return output


def run(args):
    """
    Execute the script with provided arguments

    :type args object arguments
    """
    chapter_break = '__CHAPTER__'

    publication_ids = args['ID']
    logging.info('Generating XML for publication(s): {}'.format(publication_ids))

    xml = SphinxXML()

    # schema

    # fields are full-text searchable
    xml.add_field('title')
    xml.add_field('chapter')
    xml.add_field('content')

    # attributes are accessible via SELECT queries
    xml.add_attr('title', 'string')
    xml.add_attr('chapter', 'string')
    xml.add_attr('content', 'string')
    xml.add_attr('published_year', 'int')
    xml.add_attr('publication_id', 'int')
    xml.add_attr('document_id', 'int')

    xml.start()

    for publication_id in publication_ids.split(','):
        # read index.json for the publication
        index_path = 'publications/{}/index.json'.format(publication_id)
        with open(index_path) as fp:
            publication_data = json.load(fp)

        logging.info("Got {} issues for '{}'".format(publication_data['count'], publication_data['name'].encode('utf-8')))

        # add documents
        for issue in publication_data['issues']:
            published_year = issue['year'].split('_')[-1]  # 1951_1956

            try:
                content = get_content_stream(publication_id, issue['year'], issue['id'], chapter_break=chapter_break)
            except IOError:
                logging.error('Failed opening an issue file', exc_info=True)
                continue

            # split by chapters and index them separately
            chapters = content.getvalue().split(chapter_break)

            for chapter in chapters:
                xml.add_document(
                    document_id=str(issue['id']),
                    title=issue['name'].encode('utf-8'),
                    chapter=chapter.split("\n")[0].strip(),
                    content=chapter,
                    published_year=published_year,
                    publication_id=publication_id
                )

            content.close()

    xml.end()

if __name__ == '__main__':
    run(docopt(__doc__, version='WBC v1.0'))
