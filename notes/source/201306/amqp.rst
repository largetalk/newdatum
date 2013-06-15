===================
AMQP
===================

Producer, Broker, Exchange, Routing Key, Binding, Queue, Comsumer

channel

vhost vhost有自己的名字空间和一组Exchange, 每个连接和一个vhost关连， 链接中不可以直接切换到另一个vhost

Exhange 类型:

  Fanout: 将消息路由到所有绑定的队列， 广播模式

  Direct: 根据routing key来路由信息，单播模式，default exchange: 特殊的direct交换机，声明时名字为空串， 无需绑定，客户端直接将消息投递到队列

  Topic: 采用模式匹配来路由消息， 多播模式 用.分割多个字符单元， 用#匹配0个或多个字符单元， 用*匹配一个字符单元

  Headers:

  Custom:

发布的消息元数据：

  routing_key

  persistent : 发布持久性消息

  immediate ： 不能立刻投递到消费者，返回失败

  mandatory ： 不能路由到队列，返回失败

  content_type

  content_encoding

  priority

  message_id

  correlation_id

  replay_to

  type

  user_id

  app_id

  timestamp

  expiration

队列类型：

  持久性队列：一直存在，不管有没有消费者，可以被多个消费者共享

  临时队列： 只绑定到一个消费者的私有队列，该消费者断开，队列删除

队列需要绑定到交换机， 同一交换机可以绑定多个队列

consume, subscribe 调用push api, 通知broker主动发数据

get调用GET api, 由客户端被动取数据

消息确认模式：

  自动确认： 消息发完， broker就从队列里将它移除

  显式确认模式： 有消费者决定何时发ack, broker接到ack后才从队列中删除消息， 如果发ack前， 客户端断了， broker将重新投递消息

  应用也可以发送拒绝消息，指示broker丢弃或重传
