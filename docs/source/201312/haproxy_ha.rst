==================================
使用KeepAlived实现Haproxy HA
==================================

服务器配置
================

分别在144和145上设置/etc/keepalived/keepalived.conf ::

    #172.16.21.144
    global_defs {
       notification_email {
           xxx@yyy.com
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
            #可设置多个虚拟IP，每行1个
        }
    
        track_script {
            chk_rabbitmq
        }
    }

::

    #172.16.21.145
    global_defs {
       notification_email {
           xxx@yyy.com
       }
    
       notification_email_from mail@example.org
       smtp_server 127.0.0.1
       smtp_connect_timeout 30
       router_id LVS_DEVEL
    }
    
    vrrp_script chk_haproxy {
        script "/home/dev/conf/chk_haproxy.sh" 
        interval 2
        weight -2
    }
    vrrp_instance VI_HAPROXY {
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
            172.16.21.222
            #可设置多个虚拟IP，每行1个
        }
    
        track_script {
            chk_haproxy
        }
    }

track script
=======================

/home/dev/conf/chk_haproxy.sh ::

    #!/bin/bash
    status=$(ps aux|grep haproxy |grep sbin | grep -v grep | grep -v bash | wc -l)
    if [ "${status}" = "0" ]; then
        /etc/init.d/haproxy start
    
        status2=$(ps aux|grep haproxy |grep sbin | grep -v grep | grep -v bash |wc -l)
    
        if [ "${status2}" = "0"  ]; then
                /etc/init.d/keepalived stop
        fi
    fi
