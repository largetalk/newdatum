: > _err
: > _md5
psql='psql -U ellis -h serena -t -P format=unaligned'
ls correct | while read file
do
    size=$(du -b correct/$file | awk '{print $1}')
    md5new=$(md5sum correct/$file | awk '{print $1}')
    md5old=$(md5sum wrong/$file | awk '{print $1}')
    res=$(echo "SELECT DISTINCT path FROM main_resource WHERE md5='$md5old';" | $psql)
    if [ -n "$res" ]
    then
        echo "UPDATE main_resource SET md5='$md5new', size=$size WHERE md5='$md5old';" | $psql
        echo "$res" | sed 's/\n//g' | while read path
        do
            scp correct/$file apache@serena:ellis/media/upload/$path
        done
        echo $md5new >> _md5
    else
        echo $file >> _err
    fi
done
echo

(
echo "SELECT * FROM ellis_exercise_resource_md5("
awk '{printf "\x27"$1"\x27, "}' _md5 | sed 's/, $//'
echo ");"
) | $psql
