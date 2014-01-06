=======================
MongoDB 杂事
=======================

昨天线上mongo发生一次故障，出现客户端连不上，查询巨慢等现象，排除一整天也无法复原问题出现，不过这个过程中对mongo和pymongo有更进一步了解，特此笔记。

819连接数
=======================

查看日志看到大量如下日志::

    Getting connection refused because too many open connections: 819

使用db.serverStatus().connections查看连接数::

    > db.serverStatus().connections
    { "current" : 71, "available" : 748 }
    current是当前占用的连接数， available表示空闲的

这个错误产生的原因主要是因为linux每个进程1024个文件句柄限制导致的。使用ulimit -n 或 ulimit -a 查看当前系统限制。

使用ulmit -n 65535 只会更改当前session的文件句柄限制，要更改系统的限制需vim /etc/security/limits.conf 添加如下行::

    *                soft    nofile          65535
    *                hard    nofile          65535

mongo的配置文件也需要修改 vim /etc/mongodb.conf ::

    maxConns=20000 #mongo连接数不能超过20000

ps. linux系统做服务器一般都需要做些优化，这里给出一些常用优化项，vim /etc/sysctl.conf::

    net.ipv4.tcp_max_tw_buckets = 819200
    net.ipv4.tcp_tw_recycle = 1
    net.ipv4.tcp_tw_reuse = 1
    net.ipv4.ip_local_port_range = 1024 65000
    net.ipv4.tcp_max_syn_backlog = 819200
    #net.ipv4.tcp_syncookies = 1
    net.core.somaxconn = 262144
    net.core.netdev_max_backlog = 262144
    net.ipv4.tcp_max_orphans = 262144
    net.ipv4.tcp_timestamps = 0
    net.ipv4.tcp_synack_retries = 1
    net.ipv4.tcp_syn_retries = 1
    net.ipv4.tcp_fin_timeout = 1
    net.ipv4.tcp_keepalive_time = 30
    
    net.ipv4.conf.default.rp_filter = 1
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.tcp_syncookies = 0
    net.ipv6.conf.all.disable_ipv6 = 1
    
    vm.swappiness=5

pymongo连接参数
=======================

为了解决连接数过大的问题也算是翻遍了pymongo代码，发现两个选项，能起点作用

auto_start_request: 设为True时，MongoClient为每个线程分配一个socket, 这样比较安全，它能保证你在一个unacknowledged 写之后的读也是对的。而设为False时，多个线程共用socket, 不过如果你还想在单个socket上做序列操作以保证read-your-own-writes consistency, 可以使用 start_request/end_request. 更多详情请看：http://emptysqua.re/blog/requests-in-python-and-mongodb/

use_greenlets: 为True时，使用gevent时，该参数设为True, start_request会保证当前greenlet会使用同一个socket

mongostat
========================

mongostat是个非常好用的监控工具

$mongostat ::

    insert  query update delete getmore command flushes mapped  vsize    res faults locked % idx miss %     qr|qw   ar|aw  netIn netOut  conn       time
     2      6      3      0       0       6       0  4.44g    13g   772m      0        0          0       0|0     0|0     3k    40k    71   16:12:48
    10     13     13      1       0      18       0  4.44g    13g   775m      0      0.3          0       0|0     0|0    46k    29k    71   16:12:49
     6      7      7      0       0      14       0  4.44g    13g   772m      0      0.2          0       0|0     0|0     7k     5k    71   16:12:50
     0      0      0      0       0       1       0  4.44g    13g   772m      0        0          0       0|0     0|0    62b     1k    71   16:12:51
     2      3      3      0       0       6       0  4.44g    13g   772m      0        0          0       0|0     0|0     3k     4k    71   16:12:52
    47     32     54      2       0      66       0  4.44g    13g   776m      0      1.1          0       0|0     0|0   422k   160k    71   16:12:53
     0      0      0      0       0       1       0  4.44g    13g   776m      0        0          0       0|0     0|0    62b     1k    71   16:12:54
     8     10     10      0       0      19       0  4.44g    13g   776m      0      0.1          0       0|0     0|0    11k     8k    71   16:12:55
     4      5      5      0       0      10       0  4.44g    13g   776m      0        0          0       0|0     0|0     5k     5k    71   16:12:56
     0      0      0      0       0       1       0  4.44g    13g   776m      0        0          0       0|0     0|0    62b     1k    71   16:12:57


insert/query/update/delete: 每秒 插入/查询/更新/删除数

getmore: 查询时游标的getmore操作数

command: 每秒执行命令数

flush: 一秒内flush的次数，flush开销很大，如果频繁flush, 可能需要查查原因了

mapped: 所有被mmap的数据量，单位是MB

vsize: 虚拟内存使用量

res: 物理内存使用量

faults: 每秒访问失败数（只有Linux有），数据被交换出物理内存，放到swap。不要超过100，否则就是机器内存太小，造成频繁swap写入。此时要升级内存或者扩展

locked: 写锁所占时间比，该数值过大(>10%)就需要注意了

idx miss: 索引不命中百分比，正常情况下，所有查询都应该通过索引

qr|qw ar|aw: mongo负载高时，命令来不及处理，mongo将命令放入队列。 qr|qw 等待读/写的队列长度 ar|aw 执行读/写操作客户端数量

netIn/netOut: 出入网络带宽

conn: 当前连接数

mongo command
========================

查看/创建/删除 索引 ::
   
    db.collection.getIndexes();
    db.collection.ensureIndex({x: 1})
    db.collection.dropIndexes();
    db.collection.dropIndex({x: 1})

在后台创建索引(线上数据库加索引为了不影响正常应用) ::

    db.collection.ensureIndex({x: 1, y: 1}, {background: true});

重建索引(collection大小变动巨大或索引占用过多空间时执行) ::

    db.collection.reIndex();

查看数据库信息 ::

    db.stats();

服务器状态 ::

    db.serverStatus();

mongodb 当前正在执行的操作 ::

    db.currentOp()

如果你发现一个操作太长，把数据库卡死的话，可以用这个命令杀死他 ::

    db.killOp("xxxx")


mongon内存
========================

mongo是出了名的吃内存，空间碎片问题严重，目前也没有什么好办法。

可以用db.repaireDatabase() 整理数据库，非常慢，线上系统就不要用了。

查看系统内存 ::

    free -m
                 total       used       free     shared    buffers     cached
    Mem:         15793       6879       8913          0        385       4102
    -/+ buffers/cache:       2391      13401
    Swap:         8183          0       8183

linux可用内存计算方法是free + buffers + cached, 实际使用内存是 used - buffers - cached

MongoDB使用的是内存映射存储引擎，它会把数据文件映射到内存中，如果是读操作，内存中的数据起到缓存的作用，如果是写操作，内存还可以把随机的写操作转换成顺序的写操作，总之可以大幅度提升性能。MongoDB并不干涉内存管理工作，而是把这些工作留给操作系统的虚拟内存管理器去处理，这样做的好处是简化了MongoDB的工作，但坏处是你没有方法很方便的控制MongoDB占多大内存，幸运的是虚拟内存管理器的存在让我们多数时候并不需要关心这个问题。

更多内存相关可看: http://huoding.com/2011/08/19/107

######################

top 或ps看一下mongo 

VIRT: 虚拟内存

RES: 常驻内存 这个值就是该应用程序真的使用的内存，但还有两个小问题，一是有些东西可能放在交换盘上了（SWAP），二是有些内存可能是共享的。

SHR: 共享内存 就是说这一块内存空间有可能也被其他应用程序使用着；而Virt － Shr似乎就是这个程序所要求的并且没有共享的内存空间。

DATA: 数据内存（top 按f键） 这一块是真正的该程序要求的数据空间，是真正在运行中要使用的。

使用vmtouch_ 检查文件的缓存情况 ::

    # vmtouch -m4G /var/lib/mongodb/
    Files: 26
    Directories: 3
    Resident Pages: 1690343/3685382  6G/14G  45.9%
    Elapsed: 0.3167 seconds

.. _vmtouch: https://github.com/hoytech/vmtouch

参考: http://xiezhenye.com/2013/05/mongodb-%E5%86%85%E5%AD%98%E4%BD%BF%E7%94%A8.html

ipython command
=====================

%run

%paste

%cpaste

%timeit %time

%prun  or %run -p or %lprun

%reset

%magic

ipython qtconsole --pylab=inline #ipython gui

Ctrl-R #search

%logstart %logoff %logon %logstate %logstop

!cmd  output = !cmd args

%pwd %cd %pushd %popd %dirs %bookmark

%env

%debug

