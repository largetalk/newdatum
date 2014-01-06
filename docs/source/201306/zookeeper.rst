=================================
Zookeeper集群安装
=================================

前提:准备3台机器，ip分别是

172.16.97.11

172.16.97.12

172.16.120.4

1. 下载zookeeper, http://zookeeper.apache.org/releases.html , 我下载的最新的3.4.5版

2. 下面操作在3台机器上都要做::

    sudo tar xvf zookeeper-3.4.5.tar.gz -C /opt/
    sudo mkdir -p /var/lib/zookeeper
    sudo mkdir -p /var/log/zookeeper
    cd /opt/zookeeper-3.4.5
    cp conf/zoo_sample.cfg conf/zoo.cfg

    vim conf/zoo.cfg并修改下面几行
      
        dataDir=/var/lib/zookeeper
        dataLogDir=/var/log/zookeeper
        server.1=172.16.97.11:2888:3888
        server.2=172.16.97.12:2888:3888
        server.3=172.16.120.4:2888:3888

3. 创建myid

  in 172.16.97.11
     
      echo "1" > /var/lib/zookeeper/myid

      sudo bin/zkServer.sh start
  
  in 172.16.97.12
     
      echo "2" > /var/lib/zookeeper/myid

      sudo bin/zkServer.sh start

  in 172.16.120.4
      
      echo "3" > /var/lib/Zookeeper/myid

      sudo bin/zkServer.sh start

4. connect zookeeper

   bin/zkCli.sh -server 172.16.97.11:2181
