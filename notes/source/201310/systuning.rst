========================
Linux服务器调优
========================

安装一台新的Linux服务器之后都要做些配置调整工作，优化一下系统，以前零零碎碎记录过一些，这里集中整理一下。

Linux内核参数
=======================

http://space.itpub.net/17283404/viewspace-694350

::

  net.ipv4.tcp_syncookies = 1

表示开启SYN Cookies。当出现SYN等待队列溢出时，启用cookies来处理，可防范少量SYN攻击，默认为0，表示关闭；什么是SYN Cookies: http://www.ibm.com/developerworks/cn/linux/l-syncookie/

::

  net.ipv4.tcp_tw_reuse = 1

表示开启重用。允许将TIME-WAIT sockets重新用于新的TCP连接，默认为0，表示关闭；

::

  net.ipv4.tcp_tw_recycle = 1

表示开启TCP连接中TIME-WAIT sockets的快速回收，默认为0，表示关闭。

::

  net.ipv4.tcp_fin_timeout = 30

表示如果套接字由本端要求关闭，这个参数决定了它保持在FIN-WAIT-2状态的时间。

::

  net.ipv4.tcp_keepalive_time = 1200

表示当keepalive起用的时候，TCP发送keepalive消息的频度。缺省是2小时。

::

  net.ipv4.tcp_keepalive_probes = 5

TCP发送keepalive探测以确定该连接已经断开的次数。(注意:保持连接仅在SO_KEEPALIVE套接字选项被打开是才发送.次数默认不需要修改,当然根据情形也可以适当地缩短此值.设置为5比较合适)

::

  net.ipv4.tcp_keepalive_intvl = 15

探测消息发送的频率，乘以tcp_keepalive_probes就得到对于从开始探测以来没有响应的连接杀除的时间。默认值为75秒，也就是没有活动的连接将在大约11分钟以后将被丢弃。(对于普通应用来说,这个值有一些偏大,可以根据需要改小.特别是web类服务器需要改小该值,15是个比较合适的值)

::

  net.ipv4.ip_local_port_range = 1024 65000

表示用于向外连接的端口范围。缺省情况下很小：32768到61000，改为1024到65000。

::

  net.ipv4.tcp_max_syn_backlog = 8192

表示SYN队列的长度，默认为1024，加大队列长度为8192，可以容纳更多等待连接的网络连接数。 

::

  net.ipv4.ip_conntrack_max = 655360  

在内核内存中netfilter可以同时处理的“任务”（连接跟踪条目）another voice-不要盲目增加ip_conntrack_max: http://blog.csdn.net/dog250/article/details/7107537

::

  net.ipv4.netfilter.ip_conntrack_tcp_timeout_established = 180  

跟踪的连接超时结束时间 

::

  net.ipv4.tcp_max_tw_buckets = 819200

表示系统同时保持TIME_WAIT套接字的最大数量，如果超过这个数字，TIME_WAIT套接字将立刻被清除并打印警告信息。默认为180000。设为较小数值此项参数可以控制TIME_WAIT套接字的最大数量，避免服务器被大量的TIME_WAIT套接字拖死。

::

  net.core.somaxconn = 262144

定义了系统中每一个端口最大的监听队列的长度, 对于一个经常处理新连接的高负载 web服务环境来说，默认的 128 太小了。

::

  net.core.netdev_max_backlog = 262144

该参数决定了, 每个网络接口接收数据包的速率比内核处理这些包的速率快时，允许送到队列的数据包的最大数目, 不要设的过大

::

  net.ipv4.tcp_max_orphans = 262144

系统所能处理不属于任何进程的TCP sockets最大数量。假如超过这个数量，那么不属于任何进程的连接会被立即reset，并同时显示警告信息。之所以要设定这个限制﹐纯粹为了抵御那些简单的 DoS 攻击﹐千万不要依赖这个或是人为的降低这个限制，更应该增加这个值(如果增加了内存之后)。每个孤儿套接字最多能够吃掉你64K不可交换的内存。

::

  net.ipv4.tcp_orphan_retries = 3

本端试图关闭TCP连接之前重试多少次。缺省值是7，相当于50秒~16分钟(取决于RTO)。如果你的机器是一个重载的WEB服务器，你应该考虑减低这个值，因为这样的套接字会消耗很多重要的资源。参见tcp_max_orphans.

::

  net.ipv4.tcp_timestamps = 0

时间戳,0关闭， 1开启，在(请参考RFC 1323)TCP的包头增加12个字节, 关于该配置对TIME_WAIT的影响及可能引起的问题: http://huoding.com/2012/01/19/142 , Timestamps 用在其它一些东西中﹐可以防范那些伪造的 sequence 号码。一条1G的宽带线路或许会重遇到带 out-of-line数值的旧sequence 号码(假如它是由于上次产生的)。Timestamp 会让它知道这是个 '旧封包'。(该文件表示是否启用以一种比超时重发更精确的方法（RFC 1323）来启用对 RTT 的计算；为了实现更好的性能应该启用这个选项。)

::

  net.ipv4.tcp_synack_retries = 1

tcp_synack_retries 显示或设定 Linux 核心在回应 SYN 要求时会尝试多少次重新发送初始 SYN,ACK 封包后才决定放弃。这是所谓的三段交握 (threeway handshake) 的第二个步骤。即是说系统会尝试多少次去建立由远端启始的 TCP 连线。tcp_synack_retries 的值必须为正整数，并不能超过 255。因为每一次重新发送封包都会耗费约 30 至 40 秒去等待才决定尝试下一次重新发送或决定放弃。tcp_synack_retries 的缺省值为 5，即每一个连线要在约 180 秒 (3 分钟) 后才确定逾时.

::

  net.ipv4.tcp_syn_retries = 1

对于一个新建连接，内核要发送多少个 SYN 连接请求才决定放弃。不应该大于255，默认值是5，对应于180秒左右时间。(对于大负载而物理通信良好的网络而言,这个值偏高,可修改为2.这个值仅仅是针对对外的连接,对进来的连接,是由tcp_retries1 决定的)

::

  net.ipv4.tcp_retries1 = 3

放弃回应一个TCP连接请求前﹐需要进行多少次重试。RFC 规定最低的数值是3﹐这也是默认值﹐根据RTO的值大约在3秒 - 8分钟之间。(注意:这个值同时还决定进入的syn连接)

::

  net.ipv4.tcp_retries2 = 15

在丢弃激活(已建立通讯状况)的TCP连接之前﹐需要进行多少次重试。默认值为15，根据RTO的值来决定，相当于13-30分钟(RFC1122规定，必须大于100秒).(这个值根据目前的网络设置,可以适当地改小,我的网络内修改为了5)

::

  net.ipv4.tcp_sack = 1

使 用 Selective ACK﹐它可以用来查找特定的遗失的数据报--- 因此有助于快速恢复状态。该文件表示是否启用有选择的应答（Selective Acknowledgment），这可以通过有选择地应答乱序接收到的报文来提高性能（这样可以让发送者只发送丢失的报文段）。(对于广域网通信来说这个选项应该启用，但是这会增加对 CPU 的占用。)

::

  net.ipv4.tcp_fack = 1

打开FACK拥塞避免和快速重传功能。(注意，当tcp_sack设置为0的时候，这个值即使设置为1也无效)

::

  net.ipv4.tcp_dsack = 1

允许TCP发送"两个完全相同"的SACK。

::

  net.ipv4.conf.default.rp_filter = 1
  net.ipv4.conf.all.rp_filter = 1


1 - do source validation by reversed path, as specified in RFC1812
Recommended option for single homed hosts and stub network
routers. Could cause troubles for complicated (not loop free)
networks running a slow unreliable protocol (sort of RIP),
or using static routes.

0 - No source validation.

::

  net.ipv6.conf.all.disable_ipv6 = 1
  net.ipv6.conf.default.disable_ipv6 = 1

停用 ipv6 模块

::

  vm.swappiness=5

默认60, Swappiness can be set to values between 0 and 100 inclusive. A low value means the kernel will try to avoid swapping as much as possible where a higher value instead will make the kernel aggressively try to use swap space.


others::

    # 避免放大攻击
    net.ipv4.icmp_echo_ignore_broadcasts = 1
     
    # 开启恶意icmp错误消息保护
    net.ipv4.icmp_ignore_bogus_error_responses = 1
     
    # 开启SYN洪水攻击保护
    net.ipv4.tcp_syncookies = 1
     
    # 开启并记录欺骗，源路由和重定向包
    net.ipv4.conf.all.log_martians = 1
    net.ipv4.conf.default.log_martians = 1
     
    # 处理无源路由的包
    net.ipv4.conf.all.accept_source_route = 0
    net.ipv4.conf.default.accept_source_route = 0
     
    # 开启反向路径过滤
    net.ipv4.conf.all.rp_filter = 1
    net.ipv4.conf.default.rp_filter = 1
     
    # 确保无人能修改路由表
    net.ipv4.conf.all.accept_redirects = 0
    net.ipv4.conf.default.accept_redirects = 0
    net.ipv4.conf.all.secure_redirects = 0
    net.ipv4.conf.default.secure_redirects = 0
     
    # 不充当路由器
    net.ipv4.ip_forward = 0
    net.ipv4.conf.all.send_redirects = 0
    net.ipv4.conf.default.send_redirects = 0
     
    # 开启execshild
    kernel.exec-shield = 1
    kernel.randomize_va_space = 1
     
    # IPv6设置
    net.ipv6.conf.default.router_solicitations = 0
    net.ipv6.conf.default.accept_ra_rtr_pref = 0
    net.ipv6.conf.default.accept_ra_pinfo = 0
    net.ipv6.conf.default.accept_ra_defrtr = 0
    net.ipv6.conf.default.autoconf = 0
    net.ipv6.conf.default.dad_transmits = 0
    net.ipv6.conf.default.max_addresses = 1
     
    # 优化LB使用的端口
     
    # 增加系统文件描述符限制
    fs.file-max = 65535
     
    # 允许更多的PIDs (减少滚动翻转问题); may break some programs 32768
    kernel.pid_max = 65536
     
    # 增加系统IP端口限制
    net.ipv4.ip_local_port_range = 2000 65000
     
    # 增加TCP最大缓冲区大小
    net.ipv4.tcp_rmem = 4096 87380 8388608
    net.ipv4.tcp_wmem = 4096 87380 8388608
     
    # 增加Linux自动调整TCP缓冲区限制
    # 最小，默认和最大可使用的字节数
    # 最大值不低于4MB，如果你使用非常高的BDP路径可以设置得更高
     
    # Tcp窗口等
    net.core.rmem_max = 8388608
    net.core.wmem_max = 8388608
    net.core.netdev_max_backlog = 5000
    net.ipv4.tcp_window_scaling = 1
