==========================
Flume
==========================


启动
==========================

start agent: bin/flume-ng agent -n $agent_name -c conf -f conf/flume-conf.properties.template

an example::

    # example.conf: A single-node Flume configuration

    # Name the components on this agent
    a1.sources = r1
    a1.sinks = k1
    a1.channels = c1

    # Describe/configure the source
    a1.sources.r1.type = netcat
    a1.sources.r1.bind = localhost
    a1.sources.r1.port = 44444

    # Describe the sink
    a1.sinks.k1.type = logger

    # Use a channel which buffers events in memory
    a1.channels.c1.type = memory
    a1.channels.c1.capacity = 1000
    a1.channels.c1.transactionCapacity = 100

    # Bind the source and sink to the channel
    a1.sources.r1.channels = c1
    a1.sinks.k1.channel = c1

start: bin/flume-ng agent --conf conf --conf-file example.conf --name a1 -Dflume.root.logger=INFO,console

then use telnet send message to port 44444, the original flume terminal will output the event in a log message


Third-Party plugins
========================================

plugins.d directory is located at $FLUME_HOME/plugins.d

each plugin within plugins.d can have three sub-directories:

  lib - the plugin's jar
  libext - the plugin's dependency jar
  native - any required native libraries, such as .so files

Data ingestion
======================================

Flume supports a number of mechanisms to ingest data from external sources.

  RPC
  Executing commands
  Network Stream:
    Avro
    Thrift
    Syslog
    Netcat

multi-agent flow
consolidation
multiplexing the flow

Configuration
=====================================

::

    # list the sources, sinks and channels for the agent
    <Agent>.sources = <Source>
    <Agent>.sinks = <Sink>
    <Agent>.channels = <Channel1> <Channel2>

    # set channel for source
    <Agent>.sources.<Source>.channels = <Channel1> <Channel2> ...

    # set channel for sink
    <Agent>.sinks.<Sink>.channel = <Channel1>


    # properties for sources
    <Agent>.sources.<Source>.<someProperty> = <someValue>

    # properties for channels
    <Agent>.channel.<Channel>.<someProperty> = <someValue>

    # properties for sinks
    <Agent>.sources.<Sink>.<someProperty> = <someValue>

adding multiple flows in an agent

::

    # list the sources, sinks and channels for the agent
    <Agent>.sources = <Source1> <Source2>
    <Agent>.sinks = <Sink1> <Sink2>
    <Agent>.channels = <Channel1> <Channel2>

configuration a multi agent flow

To setup a multi-tier flow, you need to have an avro/thrift sink of first hop pointing to avro/thrift source of the next hop. This will result in the first Flume agent forwarding events to the next Flume agent.

fan out flow ::

    # List the sources, sinks and channels for the agent
    <Agent>.sources = <Source1>
    <Agent>.sinks = <Sink1> <Sink2>
    <Agent>.channels = <Channel1> <Channel2>

    # set list of channels for source (separated by space)
    <Agent>.sources.<Source1>.channels = <Channel1> <Channel2>

    # set channel for sinks
    <Agent>.sinks.<Sink1>.channel = <Channel1>
    <Agent>.sinks.<Sink2>.channel = <Channel2>

    <Agent>.sources.<Source1>.selector.type = replicating

there are two models of fan out, replicating and multiplexing

multiplexing ::

    # Mapping for multiplexing selector
    <Agent>.sources.<Source1>.selector.type = multiplexing
    <Agent>.sources.<Source1>.selector.header = <someHeader>
    <Agent>.sources.<Source1>.selector.mapping.<Value1> = <Channel1>
    <Agent>.sources.<Source1>.selector.mapping.<Value2> = <Channel1> <Channel2>
    <Agent>.sources.<Source1>.selector.mapping.<Value3> = <Channel2>
    #...

    <Agent>.sources.<Source1>.selector.default = <Channel2>

Flume Source
==========================================

Avro source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be avro
    bind    –   hostname or IP address to listen on
    port    –   Port # to bind to

    ipFilter    false   Set this to true to enable ipFiltering for netty
    ipFilter.rules  –   Define N netty ipFilter pattern rules with this config.

ipFilter.rules defines N netty ipFilters separated by a comma a pattern rule must be in this format.

<’allow’ or deny>:<’ip’ or ‘name’ for computer name>:<pattern> or allow/deny:ip/name:pattern

example: ipFilter.rules=allow:ip:127.*,allow:name:localhost,deny:ip:*

Thrift source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be thrift
    bind    –   hostname or IP address to listen on
    port    –   Port # to bind to

Exec source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be exec
    command –   The command to execute

example ::

    a1.sources = r1
    a1.channels = c1
    a1.sources.r1.type = exec
    a1.sources.r1.command = tail -F /var/log/secure
    a1.sources.r1.channels = c1

JMS source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be jms
    initialContextFactory   –   Inital Context Factory, e.g: org.apache.activemq.jndi.ActiveMQInitialContextFactory
    connectionFactory   –   The JNDI name the connection factory shoulld appear as
    providerURL –   The JMS provider URL
    destinationName –   Destination name
    destinationType –   Destination type (queue or topic)

Spooling Directory Source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be spooldir.
    spoolDir    –   The directory from which to read files from.

NetCat Source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be netcat
    bind    –   Host name or IP address to bind to
    port    –   Port # to bind to

Sequence Generator Source :: 

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be seq

Syslog TCP Source :: 

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be syslogtcp
    host    –   Host name or IP address to bind to
    port    –   Port # to bind to

Multiport Syslog TCP Source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be multiport_syslogtcp
    host    –   Host name or IP address to bind to.
    ports   –   Space-separated list (one or more) of ports to bind to.

Syslog UDP Source ::

    Property Name   Default Description
    channels    –    
    type    –   The component type name, needs to be syslogudp
    host    –   Host name or IP address to bind to
    port    –   Port # to bind to

HTTP Source ::

    Property Name   Default Description
    type        The component type name, needs to be http
    port    –   The port the source should bind to.
    handler org.apache.flume.source.http.JSONHandler    The FQCN of the handler class.

JSONHandler : A handler is provided out of the box which can handle events represented in JSON format, and supports UTF-8, UTF-16 and UTF-32 character sets.

BlobHandler : BlobHandler is a handler for HTTPSource that returns an event that contains the request parameters as well as the Binary Large Object (BLOB) uploaded with this request.


Legacy Sources :

The legacy sources allow a Flume 1.x agent to receive events from Flume 0.9.4 agents. It accepts events in the Flume 0.9.4 format, converts them to the Flume 1.0 format, and stores them in the connected channel.

  Avro Legacy Source
  Thrift Legacy Source

Custom Source :

A custom source is your own implementation of the Source interface.

Scribe Source ::

    Property Name   Default Description
    type    –   The component type name, needs to be org.apache.flume.source.scribe.ScribeSource
    port    1499    Port that Scribe should be connected

Flume Sinks
====================================

HDFS Sink : 写到HDFS, 可按时间或大小分文件, 

Logger Sink : Logs event at INFO level. Typically useful for testing/debugging purpose

Avro Sink : Flume events sent to this sink are turned into Avro events and sent to the configured hostname / port pair.

Thrift Sink : This sink forms one half of Flume’s tiered collection support.

IRC Sink : The IRC sink takes messages from attached channel and relays those to configured IRC destinations.

File Roll Sink : Stores events on the local filesystem

Null Sink : Discards all events it receives from the channel.

HBaseSink ::

    Property Name   Default Description
    channel –    
    type    –   The component type name, needs to be hbase
    table   –   The name of the table in Hbase to write to.
    columnFamily    –   The column family in Hbase to write to.

AsyncHBaseSink : This sink writes data to HBase using an asynchronous model.

MorphlineSolrSink : This sink extracts data from Flume events, transforms it, and loads it in near-real-time into Apache Solr servers

ElasticSearchSink : This sink writes data to an elasticsearch cluster

Flume Channels
=============================

Memory Channel

JDBC Channel

File Channel

Spillable Memory Channel : The events are stored in an in-memory queue and on disk. This channel is currently experimental and not recommended for use in production.

Flume Channel Selectors
==============================

Replicating Channel Selector ::

    Property Name   Default Description
    selector.type   replicating The component type name, needs to be replicating
    selector.optional   –   Set of channels to be marked as optional

Multiplexing Channel Selector ::

    Property Name   Default Description
    selector.type   replicating The component type name, needs to be multiplexing
    selector.header flume.selector.header    
    selector.default    –    
    selector.mapping.*  –
