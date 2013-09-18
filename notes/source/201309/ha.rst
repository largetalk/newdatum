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

2. 编写自动化部署脚本, 安装依赖库，安装包，创建目录结构等

3. 安装nginx, 修改nginx.conf 
   
   keepalive_timeout 0; #立马关闭连接

   在upstream 下加 keepalive连接数 ::

    upstream http_backend {
        server 127.0.0.1:8080;

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

4. 启动应用

   使用gunicorn, 端口绑定到8090, A,B 两台机器一样

5. 配置nginx

   A,B 两台机器都配置nginx,都upstream到A,B 的应用8090端口

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


