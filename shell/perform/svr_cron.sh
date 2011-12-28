#!/bin/sh

la=$(uptime | awk -F'load average:' '{print $2}')
cur_time=$(date -d "today" +"%Y-%m-%d_%H:%M:%S")
mem=$(sar -r 1 1 | grep Average | awk -F":" '{print $2}')
#sar -P ALL #查看cpu
#sar -q #查看平均负载
#sar -W #页面交换状况
top1=$(top -n 1 | sed -n '/PID/{n;p}')

echo $la
echo $cur_time
echo $mem
echo $top1
