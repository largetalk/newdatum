======================
我常用的shell命令
======================

tar::

    tar jxvf filename #解压
    tar xvf filename #解压
    tar cxvf filename.tar file #压缩

wc::

    ls -l | wc -l

tr::

    ls -l | tr 'a-z' 'A-Z'

find::

    find -name "django*" -prune -o -name "*.py"
    find . -mtime -1 -type f -print
    find . -mtime -1 -type f -print0 | xargs -0 tar rvf "$archive.tar"

grep::

    ls -l | grep ^d
    ls -l | grep -n ^d
    ls -l | grep -v ^d
    echo "theaaaa
    the
    bbbbthe | grep '\<the\>'
    
    echo "theaaaa
    the
    bbbbthe | grep -A1 -B1 '\<the\>'

awk::

    ls -l | awk '{print $1}'
    echo "a|b|c" | awk -F\| '{print $1}'

sed::

    ls -l | sed 's/largetalk/root/g'
    seq 6 | sed '1!G;h;$!d'

    else:
    echo "whatever" | cat -

其他如df, top, free, uptime等就不说了

shell就是把很多小命令组合成一个大的工作，有时候还是很方便的，虽然很难看懂，奉送一个我写的shell，不算太复杂，但太长太难懂::

    ssh "$serena_user"@"$serena_host" "find /var/www/ellis/media/upload -name \*.mp3 | xargs file | grep -v Audio | awk -F: '{print \$1, \$2}' | awk -F, '{print \$1, \$4, \$5}' | awk '{if (\$4!=32 || \$6     != 22.05) print \$1, \$4, \$5, \$6, \$7}' | awk '{content=\$1;   print \$0; system(\"stat -c %s \"content)}' " > $unsuitmp3

other useful::

    lynx -dump -listonly -nonumbers http://www.verycd.com/topics/XXX/ | grep ed2k >> ed2k.txt  #爬取verycd ed2k链接

    ssh -qTfnN -D 7070 user_name@hostname  #ssh tunnel

    git remote set-url --push origin git@github.com:largetalk/datum.git
    git config remote.origin.url git@github.com:largetalk/datum.git
