#!/bin/bash

CONN='psql -U ellis --tuples-only'
(
echo "SELECT id, path, size, mime, md5 FROM main_resource WHERE mime = 'png';" | $CONN | sed 's/|//g;$d' | while read id path size mime md5
do
    echo "UPDATE main_resource SET path='$path', size=$size, mime='png', md5='$md5' WHERE id=$id;"
done
echo "UPDATE main_resource SET tag=REPLACE(tag, '.swf', '.png') WHERE mime='png' AND tag LIKE '%swf%';"
) | $CONN -h serena > /dev/null
