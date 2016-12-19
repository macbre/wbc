# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import StringIO
from os.path import dirname
from unittest import TestCase

from wbc.tidy import TextTidy


class TestTidy(TestCase):

    @staticmethod
    def tidy_fixture(fixture):
        """
        :type fixture str|unicode
        :rtype str
        """
        output = StringIO()

        with open('{}/fixtures/{}'.format(dirname(__file__), fixture), mode='rb') as fp:
            TextTidy(_in=fp, chapter_break='\n\n__CHAPTER__\n').tidy(output=output)

        return output.getvalue()

    def test_wordwrap1(self):
        text = self.tidy_fixture('138161.txt')
        print(text)

        assert 'kościół św. Jana stanie się prawdziwą atrakcją dla miłośników zabytków' in text
        assert 'plaszczyzny \ndachowej' in text

    def test_wordwrap2(self):
        text = self.tidy_fixture('138898.txt')
        print(text)

        assert 'Minikowo' in text
        assert 'pomiędzy ulicami Woźną i Wodną' in text
        assert 'i na wschód od Sródki, przy ul. Miastkowskiego.' in text

    def test_headings(self):
        text = self.tidy_fixture('case_001.txt')
        print(text)

        assert '__CHAPTER__\nBOLESŁAW KRYSIEWICZ, LEKARZ PEDIATRA I SPOŁECZNIK, PREZES NACZELNEJ RADY LUDOWEJ' in text
        assert 'działaczem Ligi Narodowej, kuratorem Okręgu Szkolnego Poznańskiego i senatorem RP.\n' + \
            'W roku 1881 zdał maturę i rozpoczął studia na Wydziale Lekarskim Uniwersytetu Wrocławskiego' in text

    def test_wordwrap_over_headings(self):
        text = self.tidy_fixture('case_002.txt')
        print(text)

        assert '__CHAPTER__\nMISTRZ MIKOŁAJ - NAJSTARSZY ZNANY LEKARZ POZNAŃSKI' in text
        assert 'gdyż nie za\nJacek Wiesiołowskiwiera on żadnych medycznych aspektów' in text
        # assert 'gdyż nie zawiera on żadnych medycznych aspektów' in text  # TODO

    def test_chapters(self):
        text = self.tidy_fixture('case_004.txt')
        print(text)

        assert 'Puch pozostał bez przywódców. Jedynie w oznaczonym dniu wykonano nieudany najazd na ' in text
        assert 'D Z I AL H I S T O R Y C Z N Y .\n\nATAK NA TWIERDZĘ POZNAŃSKĄ :-5 MARCA 1846.' in text
        assert '__CHAPTER__\nATAK NA TWIERDZĘ POZNAŃSKĄ 3 MARCA 1840.' in text
