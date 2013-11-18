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

也可以给嵌入字段/子文档添加索引， 如有 ::

    {"_id": ObjectId(...)
        "name": "John Doe"
        "address": {
            "street": "Main"
            "zipcode": 53511
            "state": "WI"
        }
    }

    db.people.ensureIndex( { "address.zipcode": 1 } )

