======================
hadoop
======================

hdfs - import and export data
====================================

hadoop fs
hadoop fs -help ls 
hadoop fs -mkdir /data/weblogs
hadoop fs -copyFromLocal welog.txt /data/weblogs
hadoop fs -ls /data/weblogs
hadoop fs -copyToLocal /data/weblogs/welog.txt ./weblog.txt
hadoop fs -getmerge /data/weblogs/weblog_md5_group.bcp ./weblog_md5_group.bcp
hadoop distcp hdfs://namenodeA/data/weblogs hdfs://namenodeB/data/weblogs
hadoop distcp –overwrite hdfs://namenodeA/data/weblogs hdfs://namenodeB/data/weblogs
hadoop distcp –update hdfs://namenodeA/data/weblogs hdfs://namenodeB/data/weblogs
hadoop distcp hftp://namenodeA:port/data/weblogs hdfs://namenodeB/data/weblogs
sqoop import -m 1 --connect jdbc:mysql://<HOST>:<PORT>/logs --username hdp_usr --password test1 --table weblogs --target-dir /data/weblogs/import
sqoop export -m 1 --connect jdbc:mysql://<HOST>:<PORT>/logs --username hdp_usr --password test1 --table weblogs_from_hdfs --export-dir /data/weblogs/05102012 --input-fields-terminated-by '\t' --mysql-delmiters

Mongo Hadoop Adaptor on GitHub : https://github.com/mongodb/mongo-hadoop

greenplum
flume

hdfs
========================================

NameNode: maintain a catalog of all block locations in the cluster
Secondary NameNode: periodically synchronizes with NameNode block index
DataNode: manages the data blocks it receives from the NameNode

LZO codec: https://github.com/kevinweil/hadoop-lzo
