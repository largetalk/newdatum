======================
Mongo ReplicaSet
======================

mongodb数据同步有两种方式

1.master,slave  

continue...

2.副本集方式(Replset)

http://my.oschina.net/zhzhenqin/blog/97268?p=1#comments

http://wenku.baidu.com/view/59f2fd3731126edb6f1a10fa.html

https://gist.github.com/millken/823610

之前测试通过使用master,slave结合keepalived进行高可用,但是方式1会有问题，即slave无法进行写操作

下面是第二种方式：

Relica Sets使用的是n个mongod节点，构建具备自动的容错功能(auto-failover),自动恢复的(auto-recovery)的高可用方案,理论上需要三个mongodb实例，在这个测试环境中，我采用的方案是2个mongod+1个arbiter。

经测试：在其中一台primary（172.16.21.38）down的时候，另外一台（172.16.21.42）自动切换为primary,可以进行读写操作

当172.16.21.38重新运行之后，切换为slave，172.16.21.42仍为primary

1.安装mongo

::

    sudo apt-get install mongodb
    设置目录权限
    $sudo mkdir -p /data/share
    sudo chown -R mongodb:mongodb /data/share

配置 /etc/mongodb.conf

::

    # mongodb.conf
    
    # Where to store the data.
    #dbpath=/var/lib/mongodb
    dbpath=/data/share/
    
    #where to log
    logpath=/var/log/mongodb/mongodb.log
    
    logappend=true
    
    bind_ip = 172.16.21.35
    #port = 27017
    replSet = myset
    # Enable journaling, http://www.mongodb.org/display/DOCS/Journaling
    journal=true

注意:journal的设置:

  journal

  Default: (on 64-bit systems) true
  
  Default: (on 32-bit systems) false


启动mongodb:

  sudo service mongodb start/restart/stop

同时在三台机器上执行以上步骤。


实例化Replica Sets
任选一个mongod节点，mongo shell 登陆进去,执行如下内容::

    > config = {_id: 'myset', members: [ 
        {_id: 0, host: '10.12.7.107:27031'}, 
        {_id: 1, host: '10.12.7.108:27032'}, 
        {_id: 2, host: '10.12.7.107:27033', arbiterOnly: true}]} 
    > rs.initiate(config) 
    > rs.conf() #查看配置信息 
    > rs.staus() 


信息::

    myset:PRIMARY> rs.status()
    {
        "set" : "myset",
        "date" : ISODate("2013-09-18T03:13:10Z"),
        "myState" : 1,
        "members" : [
            {
                "_id" : 0,
                "name" : "172.16.21.38:27017",
                "health" : 1,
                "state" : 1,
                "stateStr" : "PRIMARY",
                "uptime" : 828,
                "optime" : Timestamp(1379473640000, 1),
                "optimeDate" : ISODate("2013-09-18T03:07:20Z"),
                "self" : true
            },
            {
                "_id" : 0,
                "name" : "172.16.21.76:27017",
                "health" : 1,
                "state" : 2,
                "stateStr" : "SECONDARY",
                "uptime" : 6249,
                "optime" : Timestamp(1381720537000, 5),
                "optimeDate" : ISODate("2013-09-18T03:07:20Z"),
                "lastHeartbeat" : ISODate("2013-09-18T03:07:20Z"),
                "pingMs" : 1
            },
            {
                "_id" : 2,
                "name" : "172.16.21.35:27017",
                "health" : 1,
                "state" : 7,
                "stateStr" : "ARBITER",
                "uptime" : 828,
                "lastHeartbeat" : ISODate("2013-09-18T03:13:08Z"),
                "lastHeartbeatRecv" : ISODate("2013-09-18T03:13:08Z"),
                "pingMs" : 5
            }
        ],
        "ok" : 1
    }


客户端链接::

    conn = pymongo.Connection(host=["10.12.7.107:27031", "10.12.7.108:27032", "10.12.7.107:27033"]) 
    db = conn.test 
    post={'name':'hello world'}
    db.users.insert(post) 
    conn.disconnect() 

参考链接：

http://terrylc.blogspot.com/2013/04/mongodb-replica-set.html   

至此，看到rs.status()看到三台机器分别是PRIMARY，ARBITER，SECONDARY，

则Mongodb高可用配置完毕，下面是测试和备份处理

主从同时可以读，设置(该设置可选)：

  rs.slaveOk()

设置不可读:

  db.getMongo().setSlaveOk(false);

http://stackoverflow.com/questions/8990158/mongodb-replicates-and-error-err-not-master-and-slaveok-false-code
 

测试情况::

  A:情景:写入大数据:16Mb,主从都开启,
  过程: 写入所需2秒，在写入的时候关闭master,
  结果:数据不会写入数据库,master,slave都不包含数据，
  
  B：情景:写入标准数据(response),主从都开启
  过程:写入完立即关闭master,
  结果：检查slave不包含写入数据，此时slave切换成master
  当之前的master重新开启,则可以在slave(已经成为master)上可以查询到插入的数据
  
  mongodb写入过程：数据写入db,同时会有文件log不断检查数据库修改记录

参考链接：http://docs.mongodb.org/manual/core/replica-set-oplog/


MongoDB数据恢复：

2013-10-10mongodb数据库宕机解决方案

恢复数据::

    rm /data/db/mongod.lock
    mongod --dbpath /data/db --repair
    mongod --dbpath /data/db

恢复rollback，数据位于：/data/share/rollback/*.bson

查看bson数据内容：

bsondump collection.bson > collection.json

rollback数据：

mongorestore --collection people --db accounts dump/accounts/people.bson

如果数据存在数据库中，需要先删除再导入

参考链接：

http://docs.mongodb.org/manual/tutorial/recover-data-following-unexpected-shutdown/

http://docs.mongodb.org/manual/reference/program/bsondump/

http://docs.mongodb.org/manual/reference/program/mongorestore/#bin.mongorestore


