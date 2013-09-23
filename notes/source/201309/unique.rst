生成全局唯一Id
===========================

参考了: http://www.cnblogs.com/heyuquan/p/global-guid-identity-maxId.html

1. GUID

.. code-block:: python

    import uuid
    uuid.uuid1()

优点： 确保唯一， 速度快

缺点： 太长， 不友好, 不好索引

2. 数据库唯一索引

时间戳加上随机数，然后通过数据库做唯一性校验

.. code-block:: python

    import time
    import random
    import string
    
    m = time.strftime('%y%m%d%H%M%S') + ''.join([random.choice(string.lowercase + string.digits) for _ in range(5)])
    #检查m在数据库中是否存在，存在则重复上述过程，不存在则存入数据库并返回

优点：适合简单应用，id较短，有一定亲和力

缺点：每秒id总数有限制，并发越大性能越低, 加大数据库访问压力，需要锁表

