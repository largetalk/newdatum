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

.. code-block:: sql

    mysql> install plugin rpl_semi_sync_master soname 'semisync_master.so';
    mysql> set global rpl_semi_sync_master_enabled=1;
    mysql> set global rpl_semi_sync_master_timeout=1000;
    mysql> show global status like 'rpl%';

为了让mysql在重启时自动加载该功能，在/etc/mysql/my.cnf 加入：

    rpl_semi_sync_master_enabled=1

    rpl_semi_sync_master_timeout=1000

备选master, host3 上：

.. code-block:: sql

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

.. code-block:: sql

    mysql> install plugin rpl_semi_sync_slave soname 'semisync_slave.so';
    mysql> set global rpl_semi_sync_slave_enabled=1;

在/etc/mysql/my.cnf中加入：

    rpl_semi_sync_slave_enabled=1

在备用节点和从节点的/etc/mysql/my.cnf中加入选项：

    read_only=1 #这个设置待商榷，备选master设为read only之后，master转移到备选master后数据库不可写(有super权限的用户还是可写）

    relay_log_purge=0

-----------------------

在master上：

.. code-block:: sql

    mysql> grant replication slave on *.* to repl@'172.16.21.%' identified by 'repl';
    mysql> show master status;
    记录下 “File”和“Position”即当前主库使用的二进制日志名称和位置。

在备选master和slave上：

.. code-block:: sql

    mysql> change master to master_host="172.16.21.23",master_user="repl",master_password="repl",master_log_file="bin-log.000001",master_log_pos=255;

master_log_file 和 master_log_pos 是上面记下的东西。

在备选master上：

.. code-block:: sql

    mysql> grant replication slave on *.* to repl@'172.16.21.%' identified by 'repl';

然后在备选master和slave上：

.. code-block:: sql

    mysql>start slave；
    mysql>show slave status\G；
    # 如果 Slave_IO_Running: Yes 和 Slave_SQL_Running: Yes 则说明主从配置成功
    # 还可以到master上执行 Mysql>show global status like “rpl%”; 如果Rpl_semi_sync_master_clients 是2.说明半同步复制正常


安装MHA
=========================

下载MHA Node 0.54: https://code.google.com/p/mysql-master-ha/downloads/detail?name=mha4mysql-node_0.54-0_all.deb&can=2&q= 

和 MHA Manager 0.55: https://code.google.com/p/mysql-master-ha/downloads/detail?name=mha4mysql-manager_0.55-0_all.deb&can=2&q=  

其他版本的文件在: https://code.google.com/p/mysql-master-ha/downloads/list

先在4台机器上安装MHA Node:

.. code-block:: shell

    apt-get install libdbd-mysql-perl
    dpkg -i mha4mysql-node_0.54-0_all.deb

在manager/host1 上安装MHA Manager:

.. code-block:: shell

    apt-get install libdbd-mysql-perl
    apt-get install libconfig-tiny-perl
    apt-get install liblog-dispatch-perl
    apt-get install libparallel-forkmanager-perl
    dpkg -i mha4mysql-manager_0.55-0_all.deb
    mkdir -p /masterha/app1/

在manager上创建配置文件/etc/app1.cnf, 内容如下:

.. code-block:: python

    [server default]
    manager_workdir=/masterha/app1
    manager_log=/masterha/app1/manager.log
    #remote_workdir=/usr/local/mysql
    #mysql user and password
    user=root
    password=root
    ssh_user=root
    repl_user=repl
    repl_password=repl
    ping_interval=1
    shutdown_script=""
    #master_ip_failover_script=/usr/local/bin/master_ip_failover
    #master_ip_online_change_script=/usr/local/bin/master_ip_online_change_script
    #report_script=""

    [server1]
    hostname=master
    master_binlog_dir=/var/log/mysql
    candidate_master=1

    [server2]
    hostname=172.16.21.50
    master_binlog_dir=/var/log/mysql
    candidate_master=1
    [server3]

    hostname=172.16.21.48
    master_binlog_dir=/var/log/mysql
    no_master=1

然后给mysql赋权限, 在3台mysql机器上执行如下语句:

.. code-block:: sql

    mysql> grant all on *.* to root@'172.16.21.15' identified by 'root';
    mysql> grant all on *.* to root@'172.16.21.23' identified by 'root';
    mysql> grant all on *.* to root@'172.16.21.50' identified by 'root';
    mysql> grant all on *.* to root@'172.16.21.48' identified by 'root';

或者也可执行如下语句:

.. code-block:: sql

    mysql> grant all on *.* to root@'172.16.21.%' identified by 'root';

然后建立ssh无密码登录环境:

在manager上:

.. code-block:: shell

    ssh-keygen -t rsa
    ssh-copy-id root@172.16.21.23
    ssh-copy-id root@172.16.21.50
    ssh-copy-id root@172.16.21.48

在master上：

.. code-block:: shell

    ssh-keygen -t rsa
    ssh-copy-id root@172.16.21.50
    ssh-copy-id root@172.16.21.48

在备选master上：

.. code-block:: shell

    ssh-keygen -t rsa
    ssh-copy-id root@172.16.21.23
    ssh-copy-id root@172.16.21.48

在slave上：

.. code-block:: shell

    ssh-keygen -t rsa
    ssh-copy-id root@172.16.21.23
    ssh-copy-id root@172.16.21.50

最后在manager上执行ssh登录检查：

.. code-block:: shell

    masterha_check_ssh --conf=/etc/app1.cnf

和复制情况检查：

.. code-block:: shell

    masterha_check_repl --conf=/etc/app1.cnf

然后可以启动manager:

.. code-block:: shell

    nohup masterha_manager --conf=/etc/app1.cnf < /dev/null > /masterha/app1/manager.log 2>&1 &

检查manager状态：

.. code-block:: shell

    masterha_check_status --conf=/etc/app1.cnf

停止manager:

.. code-block:: shell

    masterha_stop --conf=/etc/app1.cnf
    # 如果不能停止， 加 --abort选项

在备选master和slave节点 crontab -e 添加计划任务

.. code-block:: shell

    00 00 * * * /usr/local/bin/purge_relay_logs –user=root –password=root –disable_relay_log_purge >> /var/log/purge_relay_logs.log 2>&1


测试和恢复MHA
------------------

manager上 tail -f /masterha/app1/manager.log 监控log

然后在master上 echo c > /proc/sysrq-trigger 使其死机

在log里可以看到master转移到备选master了

除了被动转移master,还可以手动转移master,如下：

.. code-block:: shell

    masterha_master_switch --conf=/etc/app1.cnf --master_state=dead --dead_master_host=...
    masterha_master_switch --conf=/etc/app1.cnf --master_state=alive --new_master_host=...

注：针对原来的MySQL主服务器是否已经宕机，执行命令所需的参数有所不同。

MHA有个不方便的地方是，无论宕机导致的master切换还是手动切换master, 原来的master都不在MHA架构内了，重新启动也不会加入，必须手动加入。

手动加入和上面的步骤类似，先把当前master数据复制到要加入的机器，然后change master,再start slave, 关键在做这一过程中，系统不能写入，这点要人命。

master_ip_failover, shutdown_script等脚本
-------------------------------------------------

MHA在配置文件里设置使得一些脚本在特定时候被执行

shutdown_script: MHA用于关闭master的脚本，在代码samples/scripts有一个样例脚本power_manager, 脚本详解可看:https://code.google.com/p/mysql-master-ha/wiki/Parameters#shutdown_script

master_ip_failover_script, master_ip_online_change_script: 发生在master切换的时候，为了应用继续可用，调用这两个脚本做些处理。refs:

.. code-block:: php

    说到Failover，通常有两种方式：一种是虚拟IP地址，一种是全局配置文件。
    MHA并没有限定使用哪一种方式，而是让用户自己选择，虚拟IP地址的方式会牵扯到其它的软件，这里就不赘述了，
    以下简单说说全局配置文件，以PHP为实现语言，代码如下：
    
    #!/usr/bin/env php
    <?php
    $longopts = array(
        'command:',
        'ssh_user:',
        'orig_master_host:',
        'orig_master_ip:',
        'orig_master_port:',
        'new_master_host::',
        'new_master_ip::',
        'new_master_port::',
    );
    
    $options = getopt(null, $longopts);
    
    if ($options['command'] == 'start') {
        $params = array(
            'ip'   => $options['new_master_ip'],
            'port' => $options['new_master_port'],
        );
    
        $string = '<?php return ' . var_export($params, true) . '; ?>';
    
        file_put_contents('config.php', $string, LOCK_EX);
    }
    
    exit(0);
    ?>
    注：用其它语言实现这个脚本也是OK的，最后别忘了给脚本加上可执行属性。
    
    如果要测试效果的话，可以kill掉当前的MySQL主服务器，稍等片刻，MHA就会把某台MySQL从服务器提升为新的MySQL主服务器，
    并调用master_ip_failover_script脚本，
    如上所示，我们在master_ip_failover_script脚本里可以把新的MySQL主服务器的ip和port信息持久化到配置文件里，
    这样应用就可以使用新的配置了。
    
    有时候需要手动切换MySQL主服务器，可以使用masterha_master_switch命令，
    不过它调用的不是master_ip_failover_script脚本，而是master_ip_online_change_script脚本，但调用参数类似，脚本可以互用。

虚拟ip涉及到其他软件，我们稍后讲

report_script: You might want to send a report (i.e. e-mail) when failover has completed or ended with errors. 接受如下参数：

.. code-block:: shell

    --orig_master_host=(dead master's hostname)
    --new_master_host=(new master's hostname)
    --new_slave_hosts=(new slaves' hostnames, delimited by commas)
    --subject=(mail subject)
    --body=(body)

这些脚本在代码包里都有示例，但都是perl的，你可以用其他脚本语言自己来写。

配置虚拟IP
===========================

有个简单的方法添加虚拟ip, 用ifconfig命令， 参考此文章：http://blog.csdn.net/csfreebird/article/details/7996318

添加VIP:

.. code-block:: shell

    /sbin/ifconfig eth0:1 172.16.21.119/24

删除VIP:

.. code-block:: shell

    /sbin/ifconfig eth0:1 down

把配置写入/etc/network/interfaces, 使其重启有效：

.. code-block:: shell

    auto lo  
    iface lo inet loopback  
      
    auto eth0:0  
    iface eth0:0 inet static  
    name Ethernet alias LAN card  
    address 10.112.18.191  
    netmask 255.255.255.0  
    broadcast 10.112.18.255  
    network 10.112.18.0  

网上找了一个master_ip_failover脚本就是用此方法更改VIP:

.. code-block:: perl

    #!/usr/bin/env perl
    use strict;
    use warnings FATAL => 'all';
    
    use Getopt::Long;
    
    my (
        $command,          $ssh_user,        $orig_master_host, $orig_master_ip,
        $orig_master_port, $new_master_host, $new_master_ip,    $new_master_port
    );
    
    my $vip = '172.16.21.119/24';  # Virtual IP 
    my $key = "1"; 
    my $ssh_start_vip = "/sbin/ifconfig eth0:$key $vip";
    my $ssh_stop_vip = "/sbin/ifconfig eth0:$key down";
    
    GetOptions(
        'command=s'          => \$command,
        'ssh_user=s'         => \$ssh_user,
        'orig_master_host=s' => \$orig_master_host,
        'orig_master_ip=s'   => \$orig_master_ip,
        'orig_master_port=i' => \$orig_master_port,
        'new_master_host=s'  => \$new_master_host,
        'new_master_ip=s'    => \$new_master_ip,
        'new_master_port=i'  => \$new_master_port,
    );
    
    exit &main();
    
    sub main {
    
        print "\n\nIN SCRIPT TEST====$ssh_stop_vip==$ssh_start_vip===\n\n"; 
    
        if ( $command eq "stop" || $command eq "stopssh" ) {
    
            # $orig_master_host, $orig_master_ip, $orig_master_port are passed.
            # If you manage master ip address at global catalog database,
            # invalidate orig_master_ip here.
            my $exit_code = 1;
            eval {
                print "Disabling the VIP on old master: $orig_master_host \n";
                &stop_vip();
                $exit_code = 0;
            };
            if ($@) {
                warn "Got Error: $@\n";
                exit $exit_code;
            }
            exit $exit_code;
        }
        elsif ( $command eq "start" ) {
    
            # all arguments are passed.
            # If you manage master ip address at global catalog database,
            # activate new_master_ip here.
            # You can also grant write access (create user, set read_only=0, etc) here.
            my $exit_code = 10;
            eval {
                print "Enabling the VIP - $vip on the new master - $new_master_host \n";
                &start_vip();
                $exit_code = 0;
            };
            if ($@) {
                warn $@;
                exit $exit_code;
            }
            exit $exit_code;
        }
        elsif ( $command eq "status" ) {
            print "Checking the Status of the script.. OK \n"; 
            `ssh $ssh_user\@cluster1 \" $ssh_start_vip \"`;
            exit 0;
        }
        else {
            &usage();
            exit 1;
        }
    }
    
    # A simple system call that enable the VIP on the new master 
    sub start_vip() {
        `ssh $ssh_user\@$new_master_host \" $ssh_start_vip \"`;
    }
    # A simple system call that disable the VIP on the old_master
    sub stop_vip() {
        `ssh $ssh_user\@$orig_master_host \" $ssh_stop_vip \"`;
    }
    
    sub usage {
        print
        "Usage: master_ip_failover --command=start|stop|stopssh|status --orig_master_host=host --orig_master_ip=ip --orig_master_port=port --new_master_host=host --new_master_ip=ip --new_master_port=port\n";
    }

将此复制两次到/usr/local/bin, 分别命名为master_ip_failover 和master_ip_online_change_script

然后将/etc/app1.cnf 中下面两行注释去掉：

.. code-block:: shell

    master_ip_failover_script=/usr/local/bin/master_ip_failover
    master_ip_online_change_script=/usr/local/bin/master_ip_online_change_script

