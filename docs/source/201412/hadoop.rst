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

create custom hadoop writeable and inputformat

performing common tasks using hive,pig and MapReduce
=================================================================

hive (external table):

DROP TABLE IF EXISTS weblog_entries;
CREATE EXTERNAL TABLE weblog_entries (
    md5 STRING,
    url STRING,
    request_date STRING,
    request_time STRING,
    ip STRING
)
ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t' LINES TERMINATED BY '\n'
LOCATION '/input/weblog/';

ps :

  LOCATION must point to a directory, not a file
  Dropping an external table does not delete the data stored in the table
  You can add data to the path specified by LOCATION

---------

CREATE TABLE weblog_entries_with_url_length AS
SELECT url, request_date, request_time, length(url) as url_length
FROM weblog_entries;

ps:

  CREATE TABLE AS cannot be used to create external tables
  DROP temporary tables

---------

SELECT concat_ws('_', request_date, request_time) FROM weblog_entries;

--------

SELECT wle.*, itc.country FROM weblog_entries wle JOIN ip_to_country itc ON wle.ip = itc.ip;

ps:
  Hive supports multitable joins
  The ON operator for inner joins does not support inequality conditions


Use NullWritable to avoid unnecessary serialization overhead

DistributedCache.addCacheFile(new Path("/cache_files/news_keywords.txt").toUri(), conf);""))

Use the distributed cache to pass JAR dependencies to map/reduce task JVMs

Distributed cache does not work in local jobrunner mode

advanced join
=========================

nobots_weblogs = LOAD '/user/hadoop/apache_nobots_tsv.txt' AS (ip: chararray, timestamp:long, page:chararray, http_status:int, payload_size:int, useragent:chararray);
ip_country_tbl = LOAD '/user/hadoop/nobots_ip_country_tsv.txt' AS (ip:chararray, country:chararray);
weblog_country_jnd = JOIN nobots_weblogs BY ip, ip_country_tbl BY ip USING 'replicated';

-------

weblog_country_jnd = JOIN nobots_weblogs BY ip, ip_country_tbl BY ip USING 'merge';

------

weblog_country_jnd = JOIN nobots_weblogs BY ip, ip_country_tbl BY ip USING 'skewed';

------

SELECT /*+ MAPJOIN(nh)*/ acled.event_date, acled.event_type, nh.description
FROM acled_nigeria_cleaned acled
JOIN nigeria_holidays nh
ON (substr(acled.event_date, 6) = nh.yearly_date);

-------

SELECT acled.event_date, acled.event_type, vips.name, vips.description as pers_desc, vips.birthday
FROM nigeria_vips vips
FULL OUTER JOIN acled_nigeria_cleaned acled
ON (substr(acled.event_date,6) = substr(vips.birthday,6));

Big Data Analysis
==============================

in hive:

DISTRIBUTE BY : Rows with matching column values will partition to the same reducer. When used alone, it does not guarantee sorted input to the reducer.

SORT BY : This dictates which columns to sort by when ordering reducer input records

CLUSTER BY : This is a shorthand operator to perform both SORT BY and DISTRIBUTE BY operations on a group of columns.

ORDER BY : This is similar to the traditional SQL operator. Sorted order is maintained across all of the output from every reducer. Use this with caution as it can force all of the output records to a single reducer to perform the sorting. Usage with LIMIT is strongly recommended.

Advanced Big Data Analysis
==================================

Giraph : PageRank, Single-Source Shortest-path, distributed breadth-first search
http://giraph.apache.org/
BSP : http://en.wikipedia.org/wiki/Bulk_synchronous_parallel
Pregel : http://kowshik.github.io/JPregel/pregel_paper.pdf

------------

Mahout:  

Collaborative filter

mahout recommenditembased --input /user/hadoop/books/ cleaned_book_ratings.txt --output /user/hadoop/books/recommended --usersFile /user/hadoop/books/cleaned_book_users.txt -s SIMILARITY_LOGLIKELIHOOD

clustering with apache mahout
------------------------------------

1. convert the shakespeare text documents into the hadoop sequenceFile format

mahout seqdirectory --input /user/hadoop/shakespeare_text --output /user/hadoop/shakespeare-seqdir --charset utf-8

2. convert the text contents of the SequenceFile into a vector

mahout seq2sparse --input /user/hadoop/shakespeare-seqdir --output /user/hadoop/shakespeare-sparse --namedVector -ml 80 -ng 2 -x 70 -md 1 -s 5 -wt tfidf -a org.apache.lucene.analysis.WhitespaceAnalyzer

3. Run the k-means clustering algorithm on the document vectors

mahout kmeans --input /user/hadoop/shakespeare-sparse/tfidf-vectors --output /user/hadoop/shakespeare-kmeans/clusters --clusters /user/hadoop/shakespeare-kmeans/initialclusters --maxIter 10 --numClusters 6 --clustering –overwrite

4. To check the clusters identified by Mahout, use the following command:

mahout clusterdump --seqFileDir /user/hadoop/shakespeare-kmeans/clusters/clusters-1-final --numWords 5 --dictionary /user/hadoop/shakespeare-sparse/dictionary.file-0 --dictionaryType sequencefile

sentiment classification with apache mahout
-------------------------------------------------

1. reorg file

./reorg_data.py txt_sentoken train test

2. prepare the dataset for the mahout classifer

mahout prepare20newsgroups -p train -o train_formated -a org.apache.mahout.vectorizer.DefaultAnalyzer -c UTF-8

mahout prepare20newsgroups -p test -o test_formated -a org.apache.mahout.vectorizer.DefaultAnalyzer -c UTF-8

3. Place the train_formated and test_formated folders into HDFS

hadoop fs –put train_formated /user/hadoop/

hadoop fs –put test_formated /user/hadoop/

4. train the naive Bayes classifier using the train_formated dataset

mahout trainclassifier -i /user/hadoop/train_formated -o /user/hadoop/reviews/naive-bayes-model -type bayes -ng 2 -source hdfs

5. test

mahout testclassifier -m /user/hadoop/reviews/naive-bayes-model -d prepared-test -type bayes -ng 2 -source hdfs -method sequential


Debugging
===============================

Counters

context.getCounter(BadRecords.INVALID_NUMBER_OF_COLUMNS).increment(1);

MRUnit
---

Developing and testing MapReduce jobs running in local mode
---

Enabling MapReduce jobs to skip bad records
---

SkipBadRecords.setMapperMaxSkipRecords(conf, 100);
SkipBadRecords.setReducerMaxSkipGroups(conf, 100);

or

JobConf.setMaxMapAttempts() and JobConf.setMaxReduceAttempts()

Using Counters in a streaming job
---

write data to stderr

Updating task status messages to display debugging information
---

context.setMessage("user custom message");
