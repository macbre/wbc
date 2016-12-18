"""Generates SphinxSE-compatible XML stream with documents from a given publication / set of publications

XML can then be used to index publication using SphinxSE xmlpipe2 feature

Usage:
  make_xml ID
  make_xml (-h | --help)
  make_xml --version

Arguments:
  ID            Publication ID (can be comma-separated list of IDs)

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import logging
import json

from io import StringIO
from docopt import docopt

from wbc.tidy import TextTidy
from wbc.sphinx import SphinxXML


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


def generate():
    """
    Execute the script with provided arguments
    """
    args = docopt(__doc__, version='WBC v1.0')
    logger = logging.getLogger('generate_xml')

    chapter_break = '__CHAPTER__'

    publication_ids = args['ID']
    logger.info('Generating XML for publication(s): {}'.format(publication_ids))

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

        logger.info("Got {} issues for '{}'".format(
            publication_data['count'], publication_data['name'].encode('utf-8')))

        # add documents
        for issue in publication_data['issues']:
            published_year = issue['year'].split('_')[-1]  # 1951_1956

            try:
                content = get_content_stream(publication_id, issue['year'], issue['id'], chapter_break=chapter_break)
            except IOError:
                logger.error('Failed opening an issue file', exc_info=True)
                continue

            # split by chapters and index them separately
            chapters = content.getvalue().split(chapter_break)

            for chapter in chapters:
                chapter = chapter.strip()

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
