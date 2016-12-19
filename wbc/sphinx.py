import logging

from sys import stdout
from xml.sax.saxutils import XMLGenerator


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
        self._generator.startElement(self.TAG_ROOT, {'xmlns:sphinx': 'http://sphinxsearch.com/'})

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
