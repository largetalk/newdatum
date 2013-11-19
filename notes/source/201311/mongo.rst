====================
MongoDB笔记
====================

使用mongo也有一段时间了，其中也碰到很多问题，针对这些问题都去翻了不少资料，可惜的是这些经验并没有被记录下来，所以决定写这篇笔记，记录一些还记得的问题以及一些资料记录.

Mongo索引
==================

索引类型
------------------


Mongo 共用以下几种索引类型

Default _id: 每个collection必定会有，没有mongo会自动创建

Single Field: 建立再collection单个字段上的索引

Compound Index: 多个字段组合索引

Multikey Index: 建立再某个数组字段上的索引，即被索引的内容是存在数组中。

Geospatial Index: 为有效支持地理空间坐标查询的索引. Mongo 提供两种特殊索引： 2d indexs, 2sphere indexes

Text Indexes: 支持字符串内容搜索的索引(还是beta阶段)

Hashed Indexes: 为支持基于hash的sharding (hash based sharding), mongodb提供一种叫hashed indexes的索引类型。用于索引字段的hash值，这个索引随机分布更广，但只支持完全匹配查询不支持范围查询。

索引属性
--------------------

Unique Indexes: 不允许重复

Sparse Indexes: 这个属性确保索引只包含有该索引字段的collection， 忽略那些不包含该字段的collection。

索引表现
---------------------

索引有序, ps. compound index无此行为

冗余索引: 一个查询只用一个索引，除非用了$or

Single Field Indexes
---------------------------

create: db.friends.ensureIndex({"name": 1})

也可以给嵌入字段添加索引， 如有 ::

    {"_id": ObjectId(...)
        "name": "John Doe"
        "address": {
            "street": "Main"
            "zipcode": 53511
            "state": "WI"
        }
    }

    db.people.ensureIndex( { "address.zipcode": 1 } )

给子文档添加索引, ::

    {
        _id: ObjectId("523cba3c73a8049bcdbf6007"),
        metro: {
            city: "New York",
            state: "NY"
        },
        name: "Giant Factory"
    }

    db.factories.ensureIndex( { metro: 1 } )

需要注意的是， 子文档查询需要顺序和内容完全匹配， 下句会匹配上面文档::

    db.factories.find( { metro: { city: "New York", state: "NY" } } )

而下句则不会匹配上面文档::

    db.factories.find( { metro: { state: "NY", city: "New York" } } )

Compound Indexes
--------------------------------

索引顺序::

    db.events.ensureIndex( { "username" : 1, "date" : -1 } ) 支持

    db.events.find().sort( { username: 1, date: -1 } ) 和
    db.events.find().sort( { username: -1, date: 1 } )

    不支持
    db.events.find().sort( { username: 1, date: 1 } )

索引前缀， 这个也和关系数据库索引一样， a，b，c联合索引， 使用a，b查询时会使用该索引， 使用b， c则不会

Multikey Indexes
---------------------------------

::

    {
        userid: "xyz",
        addr: [
            {zip: "10086"},
            {zip: "10000"}
        ],
    }

    db.user.ensureIndex( { "addr.zip": 1} )

Hashed Indexes
----------------------------------

tips. hashed indexes与multikey indexes不兼容

create hashed indexes::

    db.active.ensureIndex( { a: "hashed" } )

索引属性
------------------------

TTL索引

TTL索引是一种特殊索引， MongoDB可以自动删除collection中过期文档，这种机制非常适合某些消息如：机器产生的事件,日志以及只需在数据库存储一定时间的session消息。

TTL索引有以下限制::

    不支持组合索引
    索引必须建立再日期类型字段上
    如果该字段是数组， 则在索引上有多个日期类型数据，在最早的日期达到过期阈值，文档就会过期

唯一索引::

    db.addresses.ensureIndex( { "user_id": 1 }, { unique: true } )

稀疏索引::

    db.addresses.ensureIndex( { "xmpp_id": 1 }, { sparse: true } )

background创建索引::

    db.people.ensureIndex( { zipcode: 1}, {background: true} )

创建唯一索引同时删除重复数据::

    db.accounts.ensureIndex( { username: 1 }, { unique: true, dropDups: true } )

指定索引名称::

    db.products.ensureIndex( { item: 1, quantity: -1 } , { name: "inventory" } )

drop index::

    db.accounts.dropIndex( { "tax-id": 1 } )

rebuild index::

    db.collection.reIndex()

force use a index::

    db.people.find( { name: "John Doe", zipcode: { $gt: 63000 } } } ).hint( { zipcode: 1 } )

Text Search 指南
-------------------------

因为text search现在还是再beta阶段，所以先要显式开启text search特性::

    mongod --setParameter textSearchEnabled=true

在字符串或字符串数组字段上创建text索引， 如果在多个字段上创建text索引，可以显示指定字段也可以用匹配符($**) ::

    db.collection.ensureIndex(
                               {
                                 subject: "text",
                                 content: "text"
                               }
                            )

    db.collection.ensureIndex(
                               { "$**": "text" },
                               { name: "TextIndex" }
                             )

search::

    db.quotes.runCommand( "text", { search: "TOMORROW" } ) # a Term

    db.quotes.runCommand( "text", { search: "tomorrow largo" } ) #any of the search term, like OR

    db.quotes.runCommand( "text", { search: "\"and tomorrow\"" } ) #搜索匹配短语and tomorrow的

    db.quotes.runCommand( "text" , { search: "tomorrow -petty" } ) #匹配有tomorrow没有petty的

使用project选项指定返回的字段::

    db.quotes.runCommand( "text", { search: "tomorrow", project: { "src": 1 } } ) #只返回_id和src字段

使用filter选项指定其他查询条件::

    db.quotes.runCommand( "text", { search: "tomorrow", filter: { speaker : "macbeth" } } )

指定语言::

    db.quotes.runCommand( "text", { search: "amor", language: "spanish" } )


