=======================
iptables 笔记
=======================

缘起：因为打算要做MySQL双机热备的，看网上文章说要用heartbeat,keeplived之类的，heartbeat会用到ipvsadm, 看ipvsadm又把我引到了iptables, 所以看了些iptables的资料，这里做些笔记，由此看来我也是个注意力不集中的人啊。

网上讲iptables配置的文章较多，讲原理的我只看到这个：http://www.frozentux.net/iptables-tutorial/cn/iptables-tutorial-cn-1.1.19.html

不过看了下，还是不太明白，还是先上几个实例再说，后面再讲讲原理

iptables实现nat
======================

nat: network address translation, 网络地址转换， 可以叫转发，不过nat可以使源地址转换和目的地址转换

先清除已有iptables规则

.. code-block:: shell

    iptables -F #清除指定chain中的规则，如果不指定chain,则是所有chain 

    iptables -X ＃删除指定用户自定义chain,如果不指定，则是所有用户自定义chain

    iptables -Z ＃清零指定chain的包和字节计数器， 如果不指定就是所有chain

    #ps. iptables 的命令都要指定table, table有filter, nat, mangle, row, security五种，不指定默认是filter, 前三种常见，后两种少见

对来自10.1.1.0/24的数据进行nat

.. code-block:: shell

    iptables -t nat -A POSTROUTING -o eth0 -s 10.1.1.0/24 -j MASQUERADE

    #表示给nat表POSTROUTING chain添加一条规则， POSTROUTING chain用于改变出去的数据包， -s是源地址， -o表示出口，MASQUERADE是动作，解释见下：

    #MASQUERADE
    This target is only valid in the nat table, in the POSTROUTING chain.  It should only be used with 
    dynamically assigned IP  (dialup) connections: if you have a static IP address, you should use the SNAT target.  
    Masquerading is equivalent to specifying a mapping to the IP address of the interface the packet is going out, 
    but also has the effect that connections are forgotten when  the  interface goes  down.   
    This is the correct behavior when the next dialup is unlikely to have the same interface address (and hence any estab‐lished connections are lost anyway).


