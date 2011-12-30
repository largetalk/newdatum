#!/bin/sh

la=$(uptime | awk -F'load average:' '{print $2}')
cur_time=$(date -d "today" +"%Y-%m-%d_%H:%M:%S")
mem=$(sar -r 1 1 | grep Average | awk -F":" '{print $2}')
#sar -P ALL #查看cpu
#sar -q #查看平均负载
#sar -W #页面交换状况
#sar -n SOCK 5 5 #socket队列信息
top1=$(top -n 1 | sed -n '/PID/{n;p}')

net_link=$(netstat -ant | grep -v LISTEN | grep -v 3306 | wc -l)
db_link=$(netstat -ant | grep 3306 | wc -l)
link_stat=$( netstat -ant | sed  -n '3, $p' | awk '{print $6}' | sort | uniq -c)

#echo $la
#echo $cur_time
#echo $mem
#echo $top1
#echo $net_link
#echo $db_link
#echo $link_stat

echo $cur_time $la $mem $db_link $net_link $link_stat
