==================================
使用KeepAlived实现RabbitMQ HA
==================================


场景
=========================

假定我们有172.16.21.144和172.16.21.145两台RabbitMQ服务器，现在需要对外提供172.16.21.143虚IP提供服务


服务器配置
==========================

1. 安装keepalived

::

    1.下载keepalived

    http://www.keepalived.org/software/keepalived-1.2.7.tar.gz

    下载后上传到服务器，我将tar包放在/tmp下（个人习惯放在/tmp）

    2.安装软件依赖的软件包
    yum -y install gcc gcc-c++ make autoconf openssl-devel popt-devel httpd
    安装httpd非必须，我是用来apache来测试keepalived是否正常工作
    若果没有安装openssl-devel你可能会遇到这样的错误
    configure: error: 
    !!! OpenSSL is not properly installed on your system. !!!
    !!! Can not include OpenSSL headers files. !!!
    此时yum -y install openssl-devel 解决
    若果没有安装popt-devel你可能会遇到这样的错误
    error: Popt libraries is required
    此时yum -y install popt-devel 解决

    3.安装keepalived
    cd /tmp
    tar xf keepalived-1.2.7.tar.gz
    mv keepalived-1.2.7 /usr/local/keepalived
    cd /usr/local/keepalived
    ./configure
    看到下图你就距离成功不远了。
    Keepalived configuration
    ————————
    Keepalived version : 1.2.7
    Compiler : gcc
    Compiler flags : -g -O2
    Extra Lib : -lpopt -lssl -lcrypto 
    Use IPVS Framework : Yes
    IPVS sync daemon support : Yes
    IPVS use libnl : No
    Use VRRP Framework : Yes
    Use VRRP VMAC : Yes
    SNMP support : No
    Use Debug flags : No

    make
    make install

    4.配置keepalived
    ln -s /usr/local/etc/rc.d/init.d/keepalived /etc/rc.d/init.d/keepalived
    ln -s /usr/local/etc/sysconfig/keepalived /etc/sysconfig/keepalived
    ln -s /usr/local/etc/keepalived /etc/keepalived
    ln -s /usr/local/sbin/keepalived /usr/sbin/
    chkconfig –add keepalived
    chkconfig keepalived on

    在此之前主和备机操作完全一样

    5.修改配置文件vim /etc/keepalived/keepalived.conf

    ! Configuration File for keepalived

    global_defs {
    notification_email {
    acassen@firewall.loc
    failover@firewall.loc
    sysadmin@firewall.loc 
    }
    notification_email_from Alexandre.Cassen@firewall.loc
    smtp_server 127.0.0.1 
    smtp_connect_timeout 30
    router_id LVS_DEVEL
    }

    vrrp_instance VI_1 {
    state MASTER         //备机此处写BACKUP
    interface eth0
    virtual_router_id 51 //主机和备机id值一样，当同网段有其他组keepalived时id值必须不同
    priority 100  //备机写90（小于100即可）
    advert_int 1
    authentication {
    auth_type PASS
    auth_pass 1111
    }
    virtual_ipaddress {
    192.168.75.200 //虚拟ip地址，如果需要多个ip请在下一行添加
    }
    }

    当你的keepalived.conf配置文件是上述时，如果主节点ip、网卡、keepalived服务异常时虚拟ip会自动漂移到从节点。
    ! Configuration File for keepalived

    vrrp_script chk_http_port {
    script “</dev/tcp/127.0.0.1/80″
    interval 1
    weight -200
    }
    vrrp_instance VI_1 {
    interface eth0
    state MASTER
    virtual_router_id 51
    priority 100
    virtual_ipaddress {
    192.168.75.200
    }
    track_script {
    chk_http_port
    }
    }

    当你的keepalived.conf配置文件是上述时，会检测你的80端口（http服务）是否正常，如果主节点http服务异常，虚拟ip会切换到备节点。

2. 分别在144和145上设置/etc/keepalived/keepalived.conf

::

    #172.16.21.144
    global_defs {
       notification_email {
           wangxutao@ata.net.cn
       }
    
       notification_email_from mail@example.org
       smtp_server 127.0.0.1
       smtp_connect_timeout 30
       router_id LVS_DEVEL
    }
    
    vrrp_script chk_rabbitmq {
        script "/home/dev/conf/chk_rabbitmq.sh" 
        interval 2
        weight -2
    }
    vrrp_instance VI_RABBITMQ {
        state MASTER
        interface eth0
        virtual_router_id 52
        priority 101
        advert_int 1
    
        authentication {
            auth_type PASS
            auth_pass 1111
        }
    
        virtual_ipaddress {
            172.16.21.143
        }
    
        track_script {
            chk_rabbitmq
        }
    }


::

    #172.16.21.145
    global_defs {
       notification_email {
           wangxutao@ata.net.cn
       }
    
       notification_email_from mail@example.org
       smtp_server 127.0.0.1
       smtp_connect_timeout 30
       router_id LVS_DEVEL
    }
    
    vrrp_script chk_rabbitmq {
        script "/home/dev/conf/chk_rabbitmq.sh" 
        interval 2
        weight -2
    }
    vrrp_instance VI_RABBITMQ {
        state BACKUP
        interface eth0
        virtual_router_id 52
        priority 100
        advert_int 1
    
        authentication {
            auth_type PASS
            auth_pass 1111
        }
    
        virtual_ipaddress {
            172.16.21.143
        }
    
        track_script {
            chk_rabbitmq
        }
    }

3. 设置/etc/sysconfig/keepalived

   KEEPALIVED_OPTIONS="-D -d -S 0" 

4. 设置track脚本并添加执行权限

::

    #!/bin/bash
    status=$(ps aux|grep rabbitmq-server | grep -v grep | grep -v bash | wc -l)
    if [ "${status}" = "0" ]; then
        /etc/init.d/rabbitmq-server start
    
        status2=$(ps aux|grep rabbitmq-server | grep -v grep | grep -v bash |wc -l)
    
        if [ "${status2}" = "0"  ]; then
            /etc/init.d/keepalived stop
        fi
    fi

5. 设置syslog

   创建/etc/rsyslog.d/keepalived.conf

::

    # keepalived -S 0
    local0.*         /var/log/keepalived.log

6. 重启rsyslog

   sudo /etc/init.d/rsyslog restart

7. 启动keepalived

   sudo /etc/init.d/keepalived start
