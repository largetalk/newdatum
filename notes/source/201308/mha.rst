=======================
mysql-master-ha
=======================

mysql 做热备和高可用的方法有很多种， 比如：

mmm: http://mysql-mmm.org/

mha: https://code.google.com/p/mysql-master-ha/

heartbeat_brdb: http://lin128.blog.51cto.com/407924/279411 http://www.centos.bz/2012/03/achieve-drbd-high-availability-with-heartbeat/

cluster(使用ndb引擎):http://database.51cto.com/art/201008/218326.htm

双master+keeplived: http://database.51cto.com/art/201012/237204.htm

双master: http://yunnick.iteye.com/blog/1845301

这里我们不介绍其他的方式他优缺点，只介绍mha的安装过程。

首先我这篇文档参考了如下网页：

官方wiki: https://code.google.com/p/mysql-master-ha/wiki/Tutorial

使用MHA做mysql的高可用：http://qiufengy.blog.51cto.com/391990/848468

Mysql5.5部署MHA: http://ylw6006.blog.51cto.com/470441/890360

mysql High Availability -MHA: http://www.vmcd.org/2012/04/mysql-high-availability-mha/

MySQL高可用性大杀器之MHA: http://huoding.com/2011/12/18/139

mysql-mha高可用 : http://blog.chinaunix.net/uid-28437434-id-3476641.html

另外有个slide讲mha的，可以看看：http://www.slideshare.net/ylouis83/mysqlmha

准备环境
==========================================

官方文档是用了4台机器，所以我也用了4台机器，分别是：

    host1: 172.16.21.15 #manager, monitor ubuntu 13.04

    host2: 172.16.21.23 #master ubuntu 12.04 server

    hots3: 172.16.21.50 #备选master ubuntu 12.04 server

    host4: 172.16.21.48 #slave ubuntu 12.04 server

mha自己不构建复制(replication)环境，所以它可以重用以前的复制结构，关于mysql复制的拓扑结构可以参考此文章：http://blog.csdn.net/hguisu/article/details/7325124

我们这里使用mysql半同步复制(semisync)架构， 半同步复制的介绍他搭建见此：http://hzcsky.blog.51cto.com/1560073/820859 http://haiker.iteye.com/blog/1632697

mysql半同步复制需要mysql版本5.5以上，另mysql 5.6以后开源协议有变， 推荐percona: http://www.percona.com/software/percona-server 或mariadb, 不过ubuntu中用apt-get 安装软件实在是很方便，我还是使用apt-get install mysql-server-5.5 来安装mysql的。

在host2, host3, host4 安装mysql后，更改其/etc/mysql/my.cnf 添加如下内容: 

    server-id               = 1 #不同的host server_id 一定要不一样，我这里host2为1, host3 为2, host4 为3

    log_bin                 = /var/log/mysql/mysql-bin.log #为了安全，应该创建一个目录存放binlog的，不过我很懒，就放到log目录了，生产环境不能这样

    replicate_ignore_db = mysql

ps: 上面和下面所有的命令最好都使用root用户执行，我曾经使用fei root用户，最后发现很烦， 另ubuntu 默认root是不可以ssh登陆的，要先：passwd root 给root添加密码，这样root就可以ssh登陆了。

半同步复制开启
===========================================

master, host2上： 

.. code-block:: shell

    mysql> install plugin rpl_semi_sync_master soname 'semisync_master.so';
    mysql> set global rpl_semi_sync_master_enabled=1;
    mysql> set global rpl_semi_sync_master_timeout=1000;
    mysql> show global status like 'rpl%';

为了让mysql在重启时自动加载该功能，在/etc/mysql/my.cnf 加入：

    rpl_semi_sync_master_enabled=1

    rpl_semi_sync_master_timeout=1000

备选master, host3 上：

.. code-block:: shell

    mysql> install plugin rpl_semi_sync_master soname 'semisync_master.so';
    mysql> set global rpl_semi_sync_master_enabled=1;
    mysql> set global rpl_semi_sync_master_timeout=1000;
    mysql> install plugin rpl_semi_sync_slave soname 'semisync_slave.so';
    mysql> set global rpl_semi_sync_slave_enabled=1;

在/etc/mysql/my.cnf中加入：

    rpl_semi_sync_master_enabled=1
    rpl_semi_sync_master_timeout=1000
    rpl_semi_sync_slave_enabled=1


slave, host4 上：

.. code-block:: shell

    mysql> install plugin rpl_semi_sync_slave soname 'semisync_slave.so';
    mysql> set global rpl_semi_sync_slave_enabled=1;

在/etc/mysql/my.cnf中加入：

    rpl_semi_sync_slave_enabled=1

在备用节点和从节点的/etc/mysql/my.cnf中加入选项：

    read_only=1 #这个设置你待商榷，备选master设为read only之后，master转移到备选master后数据库不可写(有super权限的用户还是可写）

    relay_log_purge=0

-----------------------

在master上：

.. code-block:: shell

    mysql> grant replication slave on *.* to repl@'172.16.21.%' identified by 'repl';
    mysql> show master status;
    记录下 “File”和“Position”即当前主库使用的二进制日志名称和位置。

在备选master和slave上：

.. code-block:: shell

    mysql> change master to master_host="172.16.21.23",master_user="repl",master_password="repl",master_log_file="bin-log.000001",master_log_pos=255;

master_log_file 和 master_log_pos 是上面记下的东西。

在备选master上：

.. code-block:: shell

    mysql> grant replication slave on *.* to repl@'172.16.21.%' identified by 'repl';

然后在备选master和slave上：

.. code-block:: shell

    mysql>start slave；
    mysql>show slave status\G；
    # 如果 Slave_IO_Running: Yes 和 Slave_SQL_Running: Yes 则说明主从配置成功
    # 还可以到master上执行 Mysql>show global status like “rpl%”; 如果Rpl_semi_sync_master_clients 是2.说明半同步复制正常


安装MHA
=========================
