wbc
===

Skrypt importujący publikacje na licencji **Fair Use** w formacie DJVU
z zasobów [Wielkopolskiej Biblioteki Cyfrowej](http://www.wbc.poznan.pl/dlibra)

## Wymagania

* Python 2.7 / 3.4
* curl + ungzip
* ``djvutxt`` z pakietu ``djvulibre-bin``

```
sudo apt-get install djvulibre-bin python3-lxml

virtualenv --system-site-packages env3 -p python3
source env3/bin/activate

pip install -U -e .
```

## Pobieranie

```
fetch [--no-fetch] <ID publikacji>
```

## Struktura katalogów

```
 - publications/
   - <ID publikacji>/
     - index.json
     - issues/
       - <rocznik>
         - <ID numeru>.txt
```

## xmlpipe2

Aby wygenerować plik dla [źródła SphinxSE `xmlpipe2`](http://sphinxsearch.com/docs/current/xmlpipe2.html):

```
generate_xml 106644 | gzip -c > 106644.xml.gz
```

## Publikacje

* [Kronika Miasta Poznania](http://www.wbc.poznan.pl/dlibra/publication?id=106644)
* [Dziennik Poznański](http://www.wbc.poznan.pl/dlibra/publication?id=2290)
