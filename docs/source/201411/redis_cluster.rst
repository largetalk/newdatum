====================
redis cluster
====================

redis presharding
===================

redis shard: https://github.com/zhihu/redis-shard // client shard with python

redis faina: https://github.com/facebookarchive/redis-faina // redis performace analysis tool

simple partitioning algorithms:

Node = Hash(key) MOD N

不便于添加删除Node

handling many instances
-------------------------

be prepared to handle hundred of instance

moving instance
---------------------

You can do this without any kind of down time, using a common trick:
  Start the spare Redis instances in the new virtual machine.
  Set this instances are replicas for the old instances you want to move.
  When the initial synchronization is done and all the slaves are working, change the configuration of your clients to use the new instances.
  Elect the new instances as masters with SLAVEOF NO ONE.
  Finally shut down all the old instances.
  Upgrade your shell scripts configs with the new IP/PORT info for every instance.

hash tags
--------------------

hash string inside {} to force difference keys to be stored in the same instance

fault torlerance
-------------------

can fire four maching instead of two, and set master/slave, if something goes bad, change all the occurrences of IP address in the configuration table with another one

redis partitioning
============================

why partitioning is useful
----------------------------------------

it allows for much larger databases

it allows scaling the computational power to multiple cores and multiple computer

partitioning basics
---------------------------------

one of the simplest ways to perform partitioning is with [range partitioning]. id 0-10000 will go to instance R0, id 10000-20000 will go to instance R1...

an alternative to range partitioning is [hash partitioning]. hash function (crc32, consistent hashing)

different implementations of partitioning
------------------------------------------

client side partitioning

proxy assisted partitioning

query routing

disadvantages of partitioning
------------------------------------

operations involving multiple keys are usually not supported.

redis transactions involving multiple keys can not be used.

the partitioning granuliary is the key, so it is not possible to shard a dataset with a single huge key like a very big sorted set

when partitioning is used, data handling is more complex

adding and removing capacity can be complex

data store or cache
-------------------------------

if redis is used as a cache scaling up and down using consistent hasing is easy

if redis is used as a store, a fixed keys-to-nodes map is used, so the number of nodes must be fixed and cannot vary.

presharding
-------------------------------

start with a lot of instances since the start

implemetations of redis partitioning
-----------------------------------------

redis cluster -- in beta

twemproxy -- is a proxy developed at twitter, the suggested way to handle partitioning with redis

client supporting consistent hashing


