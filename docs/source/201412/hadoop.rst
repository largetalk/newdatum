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

SequenceFile format: SequenceFileOutputFormat

Avro serialize
thrift serialize
protocol serialize

elephant bird: https://github.com/kevinweil/elephant-bird

hdfs-site.xml <name>dfs.replication</name>

change the replication factor on a per-file basis using hadoop fs shell:
hadoop fs -setrep -w 3 /my/file
hadoop fs -setrep -w 3 -R /my/dir

hdfs-site.xml <name>dfs.block.size</name>

extracting and transforming data
=========================================

pig 

1. write a Pig UDF(user define function) that extends the Pig FilterFunc abstract class

   public class IsUseragentBot extends FilterFunc {
       @Override
       public Boolean exec(Tuple tuple) throws IOException {
       }
   }

2. create Pig script

   set mapred.cache.files '/user/hadoop/blacklist.txt#blacklist';
   set mapred.create.symlink 'yes';
   register myudfjar.jar;
   all_weblogs = LOAD '/user/hadoop/apache_tsv.txt' AS (ip:chararray, timestamp:long, page:chararray, http_status:int,payload_size:int, useragent:chararray);
   nobots_weblogs = FILTER all_weblogs BY NOT com.packt.ch3.etl.pig.IsUseragentBot(useragent);
   STORE nobots_weblogs INTO '/user/hadoop/nobots_weblogs';

3. execute

   $ ls
   $ myudfjar.jar filter_bot_traffic.pig
   $ pig –f filter_bot_traffic.pig


using pig to sort

1. load data 

   nobots_weblogs = LOAD '/user/hadoop/apache_nobots_tsv.txt' AS (ip: chararray, timestamp:long, page:chararray, http_status:int, payload_size:int, useragent:chararray);

2. order

   ordered_weblogs = ORDER nobots BY timestamp;

3. store

   STORE ordered_weblogs INTO '/user/hadoop/ordered_weblogs';

using pig to sessionize web server log

1. The UDF extends the Pig abstract class EvalFunc and implement the Pig interface Accumulator

   public class Sessionize extends EvalFunc<DataBag> implements Accumulator<DataBag> {
       private long sessionLength = 0;
       private Long lastSession = null;
       private DataBag sessionBag = null;

       public Sessionize(String seconds) {
           sessionLength = Integer.parseInt(seconds) * 1000;
           sessionBag = BagFactory.getInstance().newDefaultBag();
       }

       @Override
       public DataBag exec(Tuple tuple) throws IOException {
           accumulate(tuple);
           DataBag bag = getValue();
           cleanup();
           return bag;
       }

       @Override
       public void accumulate(Tuple tuple) throws IOException {
           if (tuple == null || tuple.size() == 0) {
               return;
           }
           DataBag inputBag = (DataBag) tuple.get(0);
           for(Tuple t: inputBag) {
           Long timestamp = (Long)t.get(1);
           if (lastSession == null) {
               sessionBag.add(t);
           }
           else if ((timestamp - lastSession) >= sessionLength) {
               sessionBag.add(t);
           }
           lastSession = timestamp;
           }
       }

       @Override
       public DataBag getValue() {
           return sessionBag;
       }

       @Override
       public void cleanup() {
           lastSession = null;
           sessionBag = BagFactory.getInstance().newDefaultBag();
       }
   }

2. create a pig script to load and group web server log records by ip

   register myjar.jar;
   define Sessionize com.packt.ch3.etl.pig.Sessionize('1800');
   nobots_weblogs = LOAD '/user/hadoop/apache_nobots_tsv.txt' AS (ip: chararray, timestamp:long, page:chararray, http_status:int, payload_size:int, useragent:chararray);
   ip_groups = GROUP nobots_weblogs BY ip;

3. write the Pig expression to order all of the records associated with a specific ip by timestamp

   sessions = FOREACH ip_groups {
     ordered_by_timestamp = ORDER nobots_weblogs BY timestamp;
     GENERATE FLATTEN(Sessionize(ordered_by_timestamp));
   }
   STORE sessions INTO '/user/jowens/sessions';

using python to extend Pig

1. install jython

   java –jar jython_installer-2.5.2.jar
   export PIG_CLASSPATH=$PIG_CLASSPATH:/path/to/jython2.5.2/jython.jar

2. write python

   #!/usr/bin/python
   @outputSchema("hits:long")
   def calculate(inputBag):
       hits = len(inputBag)
       return hits

3. create a Pig script to group all of the web server log records by ip and page. Then sedn the grouped log records to the Python function

   register 'count.py' using jython as count;
   nobots_weblogs = LOAD '/user/hadoop/apache_nobots_tsv.txt' AS (ip: chararray, timestamp:long, page:chararray, http_status:int, payload_size:int, useragent:chararray);
   ip_page_groups = GROUP nobots_weblogs BY (ip, page);
   ip_page_hits = FOREACH ip_page_groups GENERATE FLATTEN(group), count.calculate(nobots_weblogs);
   STORE ip_page_hits INTO '/user/hadoop/ip_page_hits';

custom define partition, group, sort class

    key: public class CompositeKey implements WritableComparable {}
    partition: static class CompositeKeyParitioner extends Partitioner<CompositeKey, Writable> {}
    group: static class GroupComparator extends WritableComparator {}
    sort: static class SortComparator extends WritableComparator {}

::

    Configuration conf = getConf();
    Job weblogJob = new Job(conf);
    weblogJob.setJobName("PageViews");
    weblogJob.setJarByClass(getClass());
    weblogJob.setMapperClass(PageViewMapper.class);
    weblogJob.setMapOutputKeyClass(CompositeKey.class);
    weblogJob.setMapOutputValueClass(Text.class);
    weblogJob.setPartitionerClass(CompositeKeyParitioner.class);
    weblogJob.setGroupingComparatorClass(GroupComparator.class);
    weblogJob.setSortComparatorClass(SortComparator.class);
    weblogJob.setReducerClass(PageViewReducer.class);
    weblogJob.setOutputKeyClass(Text.class);
    weblogJob.setOutputValueClass(Text.class);
    weblogJob.setInputFormatClass(TextInputFormat.class);
    weblogJob.setOutputFormatClass(TextOutputFormat.class);

hive + python

python + streaming

    #!/bin/bash
    $HADOOP_HOME/bin/hadoop jar $HADOOP_HOME/contrib/streaming/hadoop-
    streaming-0.20.2-cdh3u1.jar \
        -input /input/acled_cleaned/Nigeria_ACLED_cleaned.tsv \
        -output /output/acled_analytic_out \
        -mapper location_regains_mapper.py \
        -reducer location_regains_by_time.py \
        -file location_regains_by_time.py \
        -file location_regains_mapper.py \
        -jobconf stream.num.map.output.key.fields=2 \
        -jobconf map.output.key.field.separator=\t \
        -jobconf num.key.fields.for.partition=1 \
        -jobconf mapred.reduce.tasks=1

using multipleOutputs in MapReduce to name output files


