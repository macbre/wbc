import logging

from io import StringIO

from tidy import TextTidy

logging.basicConfig(level=logging.DEBUG)


def test(fixture):
    output = StringIO()

    with open(fixture, mode='rb') as fp:
        TextTidy(_in=fp, chapter_break='\n\n__CHAPTER__\n').tidy(output=output)

    print (output.getvalue().encode('utf-8'))

if __name__ == "__main__":
    # test('tests/fixtures/test_001.txt')  # chapter
    # test('tests/fixtures/test_002.txt')  # chapter
    # test('tests/fixtures/test_003.txt')  # chapter
    test('tests/fixtures/test_004.txt')  # chapter
    # test('publications/106644/issues/2001/168143.txt')  # KMP
    # test('publications/177804/issues/1939/172528.txt')  # Warciarz
