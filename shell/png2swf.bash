#!/bin/bash

DIR=/tmp/ellis
rm -fr $DIR
mkdir -p $DIR
cd $DIR
CONN='psql -h serena -U ellis --tuples-only'
( cd /var/www/new/; find -name \*png -exec md5sum {} + ) | sort | uniq -w33 > ls
echo "SELECT distinct md5, path FROM main_resource WHERE mime='png';" | $CONN | sed 's/^ //;s/|//;$d' | sort > db
join db ls | while read md5 path line
do
    line=${line/#.\/}
    old=${line/%.png/.swf}
    swf=$DIR/${path/%.png/.swf}
    folder=$(dirname $swf)
    [ -d $folder ] ||  mkdir -p $folder
    echo cp '"/var/www/new/'$old'"' $swf | sh 2> /dev/null
    [ $? -ne 0 ] && continue
    md5new=$(md5sum $swf | awk '{print $1}')
    size=$(du -b $swf | awk '{print $1}')
    echo "UPDATE main_resource SET path=REPLACE(path, '.png', '.swf'), mime='swf', md5='$md5new', size=$size, tag=REPLACE(tag, '.png', '.swf') WHERE md5='$md5';"
done > $DIR/update.sql
rm db ls
# These are better to be done manually.
rsync -av $DIR/ apache@serena:ellis/media/upload/
psql -h serena -U ellis < $DIR/update.sql
# Now we probably need to run filter.py.
# In case of anything wrong, please run revert.bash
