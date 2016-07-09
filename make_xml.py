#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generates SphinxSE-compatible XML stream with documents from a given publication

XML can then be used to index publication using SphinxSE xmlpipe2 feature

Usage:
  make_xml.py ID
  make_xml.py (-h | --help)
  make_xml.py --version

Arguments:
  ID            Publication ID

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


def get_content_stream(publication_id, issue_year, issue_id):
    """
    :type publication_id int
    :type issue_id int
    :type issue_year int
    :rtype StringIO
    """
    file_path = 'publications/{}/issues/{}/{}.txt'.format(publication_id, issue_year, issue_id)

    output = StringIO()

    with open(file_path, mode='rb') as fp:
        TextTidy(_in=fp).tidy(output=output)

    return output


def run(args):
    """
    Execute the script with provided arguments

    :type args object arguments
    """
    publication_id = args['ID']
    logging.info('Generating XML for publication #{}'.format(publication_id))

    xml = SphinxXML()

    # schema

    # fields are full-text searchable
    xml.add_field('title')
    xml.add_field('content')

    # attributes are accessible via SELECT queries
    xml.add_attr('title', 'string')
    xml.add_attr('content', 'string')
    xml.add_attr('published_year', 'int')
    xml.add_attr('publication_id', 'int')
    xml.add_attr('document_id', 'int')

    xml.start()

    # read index.json for the publication
    index_path = 'publications/{}/index.json'.format(publication_id)
    with open(index_path) as fp:
        publication_data = json.load(fp)

    logging.info("Got {} issues for '{}'".format(publication_data['count'], publication_data['name'].encode('utf-8')))

    # add documents
    for issue in publication_data['issues']:
        published_year = issue['year'].split('_')[-1]  # 1951_1956

        content = get_content_stream(publication_id, issue['year'], issue['id'])

        xml.add_document(
            document_id=str(issue['id']),
            title=issue['name'].encode('utf-8'),
            content=content.getvalue(),
            published_year=published_year,
            publication_id=publication_id
        )

        content.close()

    xml.end()

if __name__ == '__main__':
    # val = get_content_stream(106644, 1959, 138962).getvalue()
    # print (val.encode('utf-8'))

    run(docopt(__doc__, version='WBC v0.1'))
