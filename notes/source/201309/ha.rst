=================
网站HA笔记
=================

linux自动重启
=====================

sysctl -a #查看内核参数

vim /etc/sysctl.conf 添加 kernel.panic=10 #10秒后重启

sysctl -p

echo c > /proc/sysrq-trigger  # test, invoking kernel panic


部署应用
=======================

在多台机器上部署应用，现有2台虚拟机

  A: 172.16.21.46
  B: 172.16.21.49

1. 添加专用用户, 设置权限

2. 编写自动化部署脚本(fabric), 安装依赖库，安装包，创建目录结构等

3. 启动应用

   使用gunicorn, 端口绑定到8090, A,B 两台机器一样

4. 配置nginx

   A,B 两台机器都配置nginx,都upstream到A,B 的应用8090端口

5. 安装nginx, 修改site-enabled/xxxx.conf
   
   keepalive_timeout 0; #立马关闭连接

   在upstream 下加 keepalive连接数 ::

    upstream http_backend {
        server 127.0.0.1:8090;

        keepalive 16;
    }

    server {
        ...

        location /http/ {
            proxy_pass http://http_backend;
            proxy_next_upstream http_500 http_502 http_504 error timeout invalid_header; #当后端服务器遇到500、502、504、错误与超时，自动将请求转发给web1组的另一台服务器，达到故障转移
            proxy_http_version 1.1;
            proxy_set_header Connection "";
            ...
        }
    }

6. 安装keepalived 配置成双主模式

A ::

    global_defs {
    notification_email {
    wangzhiqing@ata.net.cn
    }
    notification_email_from baojing@ata.ent.cn
    smtp_server localhost
    smtp_connect_timeout 30
    router_id NGINX_DEVEL
    }

    vrrp_script chk_http_port {
    script "/home/uts/www/online/config/monitor_nginx.sh"
    interval 2
    weight 2
    }

    vrrp_instance VI_1 {
    state MASTER
    interface eth0
    virtual_router_id 37
    priority 100
    advert_int 1
    authentication {
    auth_type PASS
    auth_pass 1111
    }
    track_script {
    chk_http_port
    }
    virtual_ipaddress {
    172.16.21.191/24
    }
    }

    vrrp_instance VI_2 {
    state BACKUP
    interface eth0
    virtual_router_id 38
    priority 90
    advert_int 1
    authentication {
    auth_type PASS
    auth_pass 1111
    }
    track_script {
    chk_http_port
    }
    virtual_ipaddress {
    172.16.21.192/24
    }
    }


B ::

    global_defs {
    notification_email {
    wangzhiqing@ata.net.cn
    }
    notification_email_from baojing@ata.ent.cn
    smtp_server localhost
    smtp_connect_timeout 30
    router_id NGINX_DEVEL
    }
    
    vrrp_script chk_http_port {
    script "/home/uts/www/online/config/monitor_nginx.sh"
    interval 2
    weight 2
    }
    
    vrrp_instance VI_1 {
    state BACKUP
    interface eth0
    virtual_router_id 37
    priority 90
    advert_int 1
    authentication {
    auth_type PASS
    auth_pass 1111
    }
    track_script {
    chk_http_port
    }
    virtual_ipaddress {
    172.16.21.191/24
    }
    }
    
    
    vrrp_instance VI_2 {
    state MASTER
    interface eth0
    virtual_router_id 38
    priority 100
    advert_int 1
    authentication {
    auth_type PASS
    auth_pass 1111
    }
    track_script {
    chk_http_port
    }
    virtual_ipaddress {
    172.16.21.192/24
    }
    }
   
cat monitor_nginx.sh ::

    #!/bin/bash
    A=`ps -C nginx --no-header |wc -l`
    if [ $A -eq 0 ];then
        /etc/init.d/nginx restart
        sleep 3
        if [ `ps -C nginx --no-header |wc -l` -eq 0 ];then
            killall keepalived
        fi
    fi

ps. monitor_nginx.sh 要加可执行权限，否则不起作用

ps. 还可以通过添加notify_master, notify_backup, notify_fault添加keepalived切换时发送邮件功能


7. nodejs安装

https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager

.. code-block:: shell

    sudo apt-get update
    sudo apt-get install python-software-properties python g++ make
    sudo add-apt-repository ppa:chris-lea/node.js
    sudo apt-get update
    ## Your version may be different. Look for "Version:" in /var/lib/apt/lists/ppa.launchpad.net_chris-lea_node.js_[...]_Packages (ellipsised part of path varies with setup)
    sudo apt-get install nodejs=0.10.18-1chl1~precise1
    # @@ Why does one need to specify the install version? @@

安装grunt ::

    npm install -g grunt-cli
    npm install --save-dev #安装库in package.json
    grunt dev:client #compile

haproxy
===================

以前老听人说ha, hb啥的，很高深的样子，这次也洋气了一把，整了下haproxy, 其实...用过也就那么回事，当然我只是简单的配置了一下，还有很多参数需要深入学习

sudo apt-get install haproxy

我的mint默认不开启haproxy守护，改下/etc/default/haproxy, ENABLED=1

cat /etc/haproxy/haproxy.cfg::

    global
    	log 127.0.0.1	local0
    	log 127.0.0.1	local1 notice
    	maxconn 4096
    	#chroot /usr/share/haproxy
    	user haproxy
    	group haproxy
    	daemon
    	#debug
    	#quiet
    
    defaults
    	log	global
    	mode	http
    	option	httplog
    	option	dontlognull
    	retries	3
    	option redispatch
    	maxconn	2000
    	contimeout	5000
    	clitimeout	50000
    	srvtimeout	50000
    
    listen rabbit-cluster 0.0.0.0:5672
        mode tcp
        balance roundrobin
        server rabbit_1 172.16.21.46:5672 check inter 2000 rise 2 fall 3
        server rabbit_2 172.16.21.49:5672 check inter 2000 rise 2 fall 3

    listen web-cluster :80
        mode tcp
        balance roundrobin
        server app_1 172.16.21.46:80 check inter 2000 rise 2 fall 3
        server app_2 172.16.21.49:90 check inter 2000 rise 2 fall 3
    
    listen monitoring :8100
        mode http
        option httplog
        stats enable
        stats uri /haproxy
        stats refresh 5s

5672端口反向到两台rabbitmq服务器，这里rabbitmq没有作集群，原因以后说

80反向到nginx的80端， 原来用nginx作loadbalance的，现在不需要这么作了，每台机器就只代理本机的应用，这样作的好处是，添加应用服务器的时候只要改haproxy的配置即可，当然缺点也有。

8100是haproxy state端口，提供一个web界面察看各服务器状态。

这里的配置参数很多都是抄的，没有深入了解各参数的意义，后面要深入学习
    
