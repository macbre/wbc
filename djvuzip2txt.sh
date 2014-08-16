#!/bin/bash
URL=$1
DEST=$2

cd $2

curl -s $1 > issue.zip
unzip issue.zip > /dev/null
djvutxt index.djvu

cd /tmp && rm -rf $2