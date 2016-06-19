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

from sys import stdout
from xml.sax.saxutils import XMLGenerator

from docopt import docopt

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

        for key, items in self._schema.iteritems():
            for item in items:
                self._generator.ignorableWhitespace("\n\t")
                self._generator.startElement('sphinx:{}'.format(key), attrs=item)
                self._generator.endElement('sphinx:{}'.format(key))

        self._generator.ignorableWhitespace("\n")
        self._generator.endElement(self.TAG_SCHEMA)
        self._generator.ignorableWhitespace("\n\n")
        self._output.flush()

    def add_document(self, document_id, **kwargs):
        self._logger.info('Adding document #{}'.format(document_id))
        self._generator.startElement(self.TAG_DOCUMENT, {"id": str(document_id)})

        for key, val in kwargs.iteritems():
            self._generator.ignorableWhitespace("\n\t")
            self._generator.startElement(key, {})
            self._generator.characters(str(val))
            self._generator.endElement(key)

        self._generator.ignorableWhitespace("\n")
        self._generator.endElement(self.TAG_DOCUMENT)
        self._generator.ignorableWhitespace("\n\n")
        self._output.flush()

    def end(self):
        self._generator.endElement(self.TAG_ROOT)
        self._generator.endDocument()


def run(args):
    """
    Execute the script with provided arguments

    :type args object arguments
    """
    publication_id = args['ID']
    logging.info('Generating XML for publication #{}'.format(publication_id))

    xml = SphinxXML()

    # schema
    xml.add_field('title')
    xml.add_field('content')
    xml.add_attr('published_year', 'int')
    xml.add_attr('pub_id', 'int', bits='16')

    xml.start()

    # read index.json for the publication
    index_path = 'publications/{}/index.json'.format(publication_id)
    with open(index_path) as fp:
        issues = json.load(fp)['issues']

    # add documents
    for issue in issues:
        issue['year'] = issue['year'].split('_')[-1]  # 1951_1956

        content = ''  # TODO

        xml.add_document(
            document_id=issue['id'],
            title=issue['name'].encode('utf-8'),
            content=content,
            published_year=int(issue['year']),
            pub_id=publication_id
        )

    xml.end()

if __name__ == '__main__':
    run(docopt(__doc__, version='WBC v0.1'))
