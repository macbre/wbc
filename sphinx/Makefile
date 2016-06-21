index:
	indexer -c sphinx.conf --rotate wbc

start:
	searchd -c sphinx.conf

console:
	mysql -h127.0.0.1 -P 36307 --default-character-set=utf8
