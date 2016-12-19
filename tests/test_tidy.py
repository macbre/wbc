# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from unittest import TestCase

from io import StringIO
from os.path import dirname

from wbc.tidy import TextTidy


class TestTidy(TestCase):

    @staticmethod
    def tidy_fixture(fixture):
        """
        :type fixture str
        :rtype str
        """
        output = StringIO()

        with open('{}/fixtures/{}'.format(dirname(__file__), fixture), mode='rb') as fp:
            TextTidy(_in=fp, chapter_break='\n\n__CHAPTER__\n').tidy(output=output)

        return output.getvalue()

    def test_wordwrap1(self):
        text = self.tidy_fixture(b'138161.txt')
        print(text)

        assert 'kościół św. Jana stanie się prawdziwą atrakcją dla miłośników zabytków' in text
        assert 'plaszczyzny \ndachowej' in text

    def test_wordwrap2(self):
        text = self.tidy_fixture(b'138898.txt')
        print(text)

        assert 'Minikowo' in text
        assert 'pomiędzy ulicami Woźną i Wodną' in text
        assert 'i na wschód od Sródki, przy ul. Miastkowskiego.' in text
