==================
nagios
==================

nagios自身在ubuntu上的安装可参照http://nagios.sourceforge.net/docs/3_0/quickstart-ubuntu.html

NRPE安装参照http://blog.c1gstudio.com/archives/559 , 另在此之前安装libssl-dev

percona monitoring plugin 可参见http://www.percona.com/software/percona-monitoring-plugins/ , can integrate with nagios

其实我就是一个网络搬运工


安装
=================

in nagios server (ubuntu 12.04):
--------------------------------------

机器A， ip 172.16.21.119

  apt-get install libssl-dev openssl

  dpkg -L libssl-dev #see libssl.so real path

  ln -s /usr/lib/x86_64-linux-gnu/libssl.so /usr/lib/libssl.so

  apt-get install apache2 libapache2-mod-php5 build-essential libgd2-xpm-dev
  
  useradd -m -s /bin/bash nagios
  
  passwd nagios

  groupadd nagcmd

  usermod -a -G nagcmd nagios

  usermod -a -G nagcmd www-data

  mkdir ~/downloads && cd ~/downloads

  wget http://prdownloads.sourceforge.net/sourceforge/nagios/nagios-3.2.3.tar.gz

  wget https://www.nagios-plugins.org/download/nagios-plugins-1.5.tar.gz

  tar xvf nagios-3.2.3.tar.gz

  cd nagios-3.2.3

  ./configure --with-command-group=nagcmd

  make all

  make install

  make install-init

  make install-config

  make install-commandmode

  vim /usr/local/nagios/etc/objects/contacts.cfg #and change email address associated with nagiosadmin

  make install-webconf

  htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin #and remember the password

  /etc/init.d/apache2 reload

  cd ..

  tar xvf nagios-plugins-1.5.tar.gz

  cd nagios-plugins-1.5

  ./configure --with-nagios-user=nagios --with-nagios-group=nagios

  make 

  make install

  ln -s /etc/init.d/nagios /etc/rcS.d/S99nagios

  /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg

  /etc/init.d/nagios start

  cd ..

  wget http://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz

  tar xvf nrpe-2.12.tar.gz

  cd nrpe-2.12

  ./configure --prefix=/usr/local/nagios

  make all

  make install-plugin

  /usr/local/nagios/libexec/check_nrpe -H xxx.xxx.xxx.xxx #after nagios client run nrpe deamon, use this to check, xxx.xxx.xxx.xxx is client ip

  vim /usr/local/nagios/etc/objects/commands.cfg , add::
    
      # 'check_nrpe ' command definition
      define command{
          command_name check_nrpe
          command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -c $ARG1$
          }

  vim /usr/local/nagios/etc/objects/hostA.cfg , add::

      define host{
          use                   generic-server ;is checkconfig error, use linux-server instead
          host_name             uts-app-2
          alias                 uts-app-2
          address               172.16.21.59
          }

      define service{
          use   generic-service
          host_name  uts-app-2
          service_description load
          check_command  check_nrpe!check_load
          }

  echo "cfg_file=/usr/local/nagios/etc/objects/hostA.cfg" >> /usr/local/nagios/etc/nagios.cfg

  service nagios reload


see nagios web interface at http://localhost/nagios/


in nagios client(ubuntu 12.04):
--------------------------------------

机器B, ip 172.16.21.59

  apt-get install libssl-dev openssl

  dpkg -L libssl-dev #see libssl.so real path

  ln -s /usr/lib/x86_64-linux-gnu/libssl.so /usr/lib/libssl.so

  groupadd nagios

  useradd -g nagios -d /usr/local/nagios -s /sbin/nologin nagios

  wget https://www.nagios-plugins.org/download/nagios-plugins-1.5.tar.gz

  tar xvf nagios-plugins-1.5.tar.gz

  cd nagios-plugins-1.5

  ./configure --with-nagios-user=nagios --with-nagios-group=nagios --prefix=/usr/local/nagios --with-ping-command="/bin/ping" 

  make 

  make install

  ls /usr/local/nagios/libexec #check

  cd ..

  wget http://sourceforge.net/projects/nagios/files/nrpe-2.x/nrpe-2.15/nrpe-2.15.tar.gz

  tar xvf nrpe-2.12.tar.gz

  cd nrpe-2.12

  ./configure --prefix=/usr/local/nagios

  make all

  make install-plugin

  make install-daemon

  make install-daemon-config

  chown -R nagios:nagios /usr/local/nagios

  vi /usr/local/nagios/etc/nrpe.cfg

    allowed_hosts=127.0.0.1,172.16.21.119

  echo 'nrpe:192.172.16.21.119' >> /etc/hosts.allow

  /usr/local/nagios/bin/nrpe -c /usr/local/nagios/etc/nrpe.cfg -d

  /usr/local/nagios/libexec/check_nrpe -H 127.0.0.1 #check

  netstat -an | grep 5666 #check

  echo "/usr/local/nagios/bin/nrpe -c /usr/local/nagios/etc/nrpe.cfg -d" >> /etc/rc.local #开机启动

some additions
-------------------------

:: 

    如何修改nrpe端口
    被监控机nrpe.cfg修改server_port为15666
    /usr/local/nagios/libexec/check_nrpe -p 15666 -H 127.0.0.1
    
    server_port=15666
    重启nrpe
    
    监控机commands.cfg增加-p 15666
    
    define command{
            command_name check_nrpe
            command_line $USER1$/check_nrpe -H $HOSTADDRESS$ -p 15666 -c $ARG1$
            }
    重启nagios就可以了
    
    Connection refused or timed out 
    检查nrpe 端口
    检查nrpe.cfg中allowed_hosts是否包含监控机ip地址
    检查/etc/hosts.allow文件中监控机ip地址nrpe:192.168.1.91
    检查iptables
    
    开放5666端口
    
    iptables -L
    iptables -A RH-Firewall-1-INPUT -p tcp -m state --state NEW -m tcp --dport 5666 -j ACCEPT
    #注意顺序
    iptables -L
    service iptables save
    service iptables restart

添加更多监控项
===============================

以添加check_procs举例

B:

  vim /usr/local/nagios/etc/nrpe.cfg ,add ::

      command[check_procs]=/usr/local/nagios/libexec/check_procs -w 5:100 -c 2:1024

  ps aux | grep nagios
  
  kill -9 xxxx #xxxx is nagios pid
  
  /usr/local/nagios/bin/nrpe -c /usr/local/nagios/etc/nrpe.cfg -d #重启

A:

  vim /usr/local/nagios/etc/objects/hostA.cfg ,add ::

      define service{
          use   generic-service
          host_name  uts-app-2
          service_description procs
          check_command  check_nrpe!check_procs
          }

  service nagios reload

   
