=================
搜索引擎漫游
=================

深夜看一些xapian的资料, 写的很细致，回想自己浏览过的lucene, solr, sphinx, elasticsearch, 均是浅尝辄止，也没留下什么东西，过后即忘，心中甚是不安，于是决定写点搜索引擎相关的知识，以补心中之憾。

ps. xapian资料: http://blog.csdn.net/visualcatsharp/article/details/4213659

搜索引擎原理
==================

初识搜索引擎应该是吴军博士的《数学之美》, 知道了 索引，倒排索引，pagerank, 也知道了搜索引擎系统的三个标准：召回率、准确率与查询效率。

举个例子，一个数据库有500个文档，其中有50个文档符合定义的问题。系统检索到75个文档，但是只有45个符合定义的问题。

召回率R=45/50=90%

精度P=45/75=60%
