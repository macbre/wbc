from io import StringIO

from tidy import TextTidy


def test_001():
    output = StringIO()

    with open('tests/fixtures/test_001.txt', mode='rb') as fp:
        TextTidy(_in=fp, chapter_break='\n\n__CHAPTER__\n').tidy(output=output)

    print (output.getvalue())


def test_002():
    output = StringIO()

    with open('publications/106644/issues/2001/168143.txt', mode='rb') as fp:
    # with open('tests/fixtures/test_002.txt', mode='rb') as fp:
        TextTidy(_in=fp, chapter_break='\n\n__CHAPTER__\n').tidy(output=output)

    print (output.getvalue())


if __name__ == "__main__":
    # test_001()
    test_002()
