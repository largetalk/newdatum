====================================================
struct -- Interpret string as packed binary data
====================================================

http://docs.python.org/2/library/struct.html

这个模块用python字符串的形式作python values和C structs之间的转换。他可被用于存储于文件或来自网络连接或其他来源的二进制数据。他使用紧凑形式的Fromat string描述C structs布局， 并据此转换成python values或将python values转换成C structs

Functions and Exceptions
=================================

struct.pack(fmt, v1, v2, ...)

    返回根据指定格式打包v1,v2,...后的字符串，values和格式(fmt)必须一一对应。

struct.pack_into(fmt, buffer, offset, v1, v2, ...)

    根据指定格式将v1,v2,...打包，将打包生成的字节写入可写的buffer,从offset开始。offset参数是必须的。

struct.unpack(fmt, string)

    根据格式解包字符串, 返回值是一个tuple即便只有一个元素，string必须准确包含format所需要的数据(len(string) == calcsize(fmt))

struct.upack_from(fmt, buffer[, offset=0])

    从buffer解包，(len(buffer[offset:]) >= calcsize(fmt))

strct.calcsize(fmt):

    返回格式对应struct的size

Format Strings
========================

字节序，大小和对齐 ::

    Character   Byte order              Size        Alignment
    @           native                  native      native
    =           native                  standard    none
    <           little-endian           standard    none
    >           big-endian              standard    none
    !           network (= big-endian)  standard    none

如果第一个字符不是上面任一个，默认是'@'

格式字符 

======  ==================   =================   =============  
Format  C Type               Python type         Standard size  
======  ==================   =================   =============  
x       pad byte             no value         
c       char                 string of length    1              
b       signed char          integer             1              
B       unsigned char        integer             1              
?       _Bool                bool                1              
h       short                integer             2              
H       unsigned short       integer             2              
i       int                  integer             4              
I       unsigned int         integer             4              
l       long                 integer             4              
L       unsigned long        integer             4              
q       long long            integer             8              
Q       unsigned long long   integer             8              
f       float                float               4              
d       double               float               8              
s       char[]               string                             
p       char[]               string                             
P       void *               integer                            
======  ==================   =================   =============  


例子

一个打包/解包的简单例子 ::

    >>> from struct import *
    >>> pack('hhl', 1, 2, 3)
    '\x00\x01\x00\x02\x00\x00\x00\x03'
    >>> unpack('hhl', '\x00\x01\x00\x02\x00\x00\x00\x03')
    (1, 2, 3)
    >>> calcsize('hhl')
    8

返回值是tuple ::

    >>> record = 'raymond   \x32\x12\x08\x01\x08'
    >>> name, serialnum, school, gradelevel = unpack('<10sHHb', record)
    
    >>> from collections import namedtuple
    >>> Student = namedtuple('Student', 'name serialnum school gradelevel')
    >>> Student._make(unpack('<10sHHb', record))
    Student(name='raymond   ', serialnum=4658, school=264, gradelevel=8)

对齐 ::

    >>> pack('ci', '*', 0x12131415)
    '*\x00\x00\x00\x12\x13\x14\x15'
    >>> pack('ic', 0x12131415, '*')
    '\x12\x13\x14\x15*'
    >>> calcsize('ci')
    8
    >>> calcsize('ic')
    5
