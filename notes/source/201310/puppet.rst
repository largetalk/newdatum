==================
Puppet
==================

安装
===========

在puppet client机器上::

    sudo apt-get install puppet


在puppet master机器上::

    sudo apt-get install puppetmaster #ubuntu

    emerge -av app-admin/puppet #gentoo

在这之前先修改好client和server的hostname， 把master的ip加入client的/etc/hosts中。

启动puppet master::

    #gentoo
    rc-service puppet start #启动agent程序, 也可以不执行此句
    rc-update add puppet default #添加开机启动

    rc-service puppetmaster start #启动puppet master程序
    rc-update add puppetmaster default

    rc-update show
    rc-status
    netstat -lpnut #查看打开的端口，默认是8140端口

启动好master之后就准备开始启动client上的puppet了，在这之前先要解决master和client之间通信证书问题

在client机器上:

vim /etc/puppet/puppet.conf 添加下面两行::

    [agent]
    server = server.puppet.com #puppet master hostname

然后执行::

    puppet agent -t

然后在puppet master机器上就可以看到client的证书请求::

    puppet cert --list
    puppet cert -s -a #对client证书进行签名
    puppert cert list --all #查看所有证书

现在就可以启动client的puppet daemon了

vim /etc/default/puppet, 把START=no改为START=yes

::

    #ubuntu
    service puppet start
    puppet agent -t --summarize #查看报告

使用
============================

安装好之后，就可以用puppet来帮助我们管理计算机了。puppet是基于c/s架构，服务端存储配置代码，然后根据客户端信息编译成相应“伪代码”传给客户端， 客户端按此对服务器进行配置，例如软件包管理，用户管理和文件管理。

puppet把控制的对象都称为资源，有文件资源file，软件包package， 系统服务service， 定期任务cron， 命令exec， 具体语法请查看官方文档

puppet执行的代码从/etc/puppet/manifests/site.pp开始

网上有很多别人写好的puppet代码，很多模块不用自己，拿来用就可以， Example42就这样一个开源模块集合，git地址是: https://github.com/example42/puppet-modules

使用如下::

    把上面的 Example42 代码移到 /etc/puppet 目录，然后修改 Puppet 服务器的配置，加上 puppet-modules 模块路径，别忘了重启 puppetmaster 服务
    # mv puppet-modules /etc/puppet
    # vi /etc/puppet/puppet.conf
    ...
    [master]
        modulepath = /etc/puppet/puppet-modules

     # /etc/init.d/puppetmaster restart

from: http://www.vpsee.com/2012/05/using-puppet-modules-from-example42/
