==================
Apache Kafka
==================

kafka characteristics:

  persistent messaging
  high throughput
  distributed
  multiple client support
  real time

install:
  single node - single broker
  single node - multiple broker
  multiple node - multiple broker

kafka broker property list:

  broker.id
  log.dirs
  zookeeper.connect

each consumer is represented as a process and these processes are organized within groups called [consumer groups].

by kafka design, the message state of any consumed message is maintained within the message consumer.

kafka desing facts:
  
  the fundamental backbone of kafka is message caching and storing it on the filesystem
  kafka provide longer retention of messages ever after consumption, allowing consumers to reconsume, if required
  kafka use a message set to group message to allow lesser network overhead
  the state of the consumed messages is maintained at consumer level
  in kafka, producers and consumers work on the traditional push-and-pull model
  kafka does not have any concept of a master and treats all the brokers as peers
  in kafka 0.8x, load balancing is achieved through kafka metadata api
  producers also have an option to choose between asynchronous or synchronous model for send message to a broker

kafka compression in kafka

  data is compressed by message producer using either gzip or snappy
