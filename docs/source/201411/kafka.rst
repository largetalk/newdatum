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

writing producers
==========================

simple producer::
  import kafka.javaapi.producer.Producer;
  import kafka.producer.KeyedMessage;
  import kafka.producer.ProducerConfig;

  Properties props = new Properties();
  props.put("metadata.broker.list","localhost:9092");
  props.put("serializer.class","kafka.serializer.StringEncoder");
  props.put("request.required.acks", "1");
  ProducerConfig config = new ProducerConfig(props);
  Producer<Integer, String> producer = new Producer<Integer, String>(config);

  String messageStr = new String("Hello from Java Producer");
  KeyedMessage<Integer, String> data = new KeyedMessage<Integer, String>(topic, messageStr);
  producer.send(data);

simple producer with message partitioning::

  Properties props = new Properties();
  props.put("metadata.broker.list","localhost:9092, localhost:9093");
  props.put("serializer.class","kafka.serializer.StringEncoder");
  props.put("partitioner.class", "test.kafka.SimplePartitioner");
  props.put("request.required.acks", "1");
  ProducerConfig config = new ProducerConfig(props);
  Producer<Integer, String> producer = new Producer<Integer, String>(config);

the kafka producer property list:

  metadata.broker.list
  serializer.class
  producer.type
  request.required.acks
  key.serializer.class
  partitioner.class

writing consumers
===========================

classes that are imported to write java-based basic consumers using the high-level consumer api for kafka cluster:

  KafkaStream
  ConsumerConfig
  ConsumerConnector

simple consumer api:

  SimpleConsumer

simple high-level java consumer::

  import kafka.consumer.ConsumerConfig;
  import kafka.consumer.KafkaStream;
  import kafka.javaapi.consumer.ConsumerConnector;

  Properties props = new Properties();
  props.put("zookeeper.connect", "localhost:2181");
  props.put("group.id", "testgroup");
  props.put("zookeeper.session.timeout.ms", "500");
  props.put("zookeeper.sync.time.ms", "250");
  props.put("auto.commit.interval.ms", "1000");
  consumer = Consumer.createJavaConsumerConnector(new ConsumerConfig(props));

  Map<String, Integer> topicCount = new HashMap<String, Integer>();
  // Define single thread for topic
  topicCount.put(topic, new Integer(1));
  Map<String, List<KafkaStream<byte[], byte[]>>> consumerStreams = consumer.createMessageStreams(topicCount);
  List<KafkaStream<byte[], byte[]>> streams = consumerStreams.get(topic);
  for (final KafkaStream stream : streams) {
    ConsumerIterator<byte[], byte[]> consumerIte = stream.iterator();
    while (consumerIte.hasNext())
      System.out.println("Message from Single Topic :: " + new String(consumerIte.next().message()));
  }
  if (consumer != null)
    consumer.shutdown();

multithreaded consumer for multipartition topics::
  Map<String, Integer> topicCount = new HashMap<String, Integer>();
  topicCount.put(topic, new Integer(threadCount));
  Map<String, List<KafkaStream<byte[], byte[]>>> consumerStreams = consumer.createMessageStreams(topicCount);
  List<KafkaStream<byte[], byte[]>> streams = consumerStreams.get(topic);
  // Launching the thread pool
  executor = Executors.newFixedThreadPool(threadCount);
 
kafka consumer property list:

  group.id
  zookeeper.connect
  client.id
  zookeeper.session.timeout.ms
  zookeeper.connection.timeout.ms
  zookeeper.sync.time.ms
  auto.commit.interval.ms

kafka integrations
=========================

kafka integration with storm

kafka integration with hadoop

kafka tools
======================

bin/kafka-create-topic.sh --zookeeper localhost:2181 --replica 3 --partition 2 --topic kafkatopic

bin/kafka-list-topic.sh --zookeeper localhost:2181

bin/kafka-run-class.sh kafka.admin.ShutdownBroker --zookeeper <zookeeper_host:port/namespace> --broker <brokerID>

bin/kafka-preferred-replica-election.sh --zookeeper <zookeeper_host:port/namespace>

