index:
	indexer -c sphinx.conf --rotate wbc

start:
	searchd -c sphinx.conf

console:
	mysql -h127.0.0.1 -P 36307 --default-character-set=utf8

search:
	mysql -h127.0.0.1 -P 36307 --default-character-set=utf8 -e "select id, SNIPPET(title, '$(q)', 'limit=75') as name, SNIPPET(content, '$(q)', 'limit=500') as snippet, published_year, pub_id  from wbc where match( '$(q)' ) order by published_year ASC limit 50" --vertical | less
