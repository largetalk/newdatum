===================
网络那些事
===================

IT从业者不接触网络的好像很少，无论实际工作还是面试，网络基础知识都需要了解。这次我们就从高层应用开发者来聊聊应该要掌握的网络知识。首先说网络就要从OSI七层模型和tcp/ip协议说起，然后往细的方向说就是三次握手，四次挥手，协议栈，CSMA/CD等内容，这方面不是我这篇文章的主要内容，不过后面如有涉及也会略微介绍一二。再就是往应用方向讲，网络的基础知识有tcp/udp, select/epoll, 同步/异步等, 再往上就是各网络库libev, libevent等和更高的协议如http等。

ok,那先从OSI七层模型说起，osi七层模型是一个逻辑上的规范，把网络分层了七层：(物理层，数据链路层，网络层，传输层，会话层，表示层，应用层), 协议分的挺清晰的，不过既然说了是逻辑上的规范，那说明实际上我们不是按照这个来干的, 实际上我们使用的TCP/IP模型， 它只有四层(网络访问层，网际互联层，传输层和应用层), 模型名称来源于模型中最重要的两个协议tcp协议和ip协议, tcp协议工作在传输层，对应osi的传输层，ip协议工作在网际互联层，对应osi的网络层， http属于应用层

tcp/ip协议是一个协议簇，经常见的有tcp， udp， ip， arp等

tcp：
