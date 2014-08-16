wbc
===

Skrypt importujący publikacje na licencji **Fair Use** w formacie DJVU
z zasobów [Wielkopolskiej Biblioteki Cyfrowej](http://www.wbc.poznan.pl/dlibra)

## Wymagania

* Python 2.6+
* curl + ungzip
* ``djvutxt`` z pakietu ``djvulibre-bin``

```
sudo apt-get install djvulibre-bin python-lxml
sudo pip install -r requirements.txt
```

## Pobieranie

```
./fetch.py <ID publikacji>
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

## Publikacje

* [Kronika Miasta Poznania](http://www.wbc.poznan.pl/dlibra/publication?id=106644)

