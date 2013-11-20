================
lua
================

先安装官网安装好lua解释器

lua类型
=================

lua是动态类型语言，变量无须定义

Numbers:

.. code-block:: lua

    >a = 1
    >b = a*10
    >print(b)
    >c = 0.7
    >print(c)

Strings:

.. code-block:: lua

    >print("hello")
    >who = 'lua user' -- 字符串可以使用"或'
    >print(who)
    >print("hello " .. who)  -- 拼接字符串使用 .. 而不是 +

Boolean:

.. code-block:: lua

    >x = true
    >print(not x)
    >print(1 == 0)
    >print(true ~= false)

Tables:

table是一种集合数据类型，集合数据类型用以存放collection(如list, set, arrays和联合数组<associative arrays>), collection包含其他对象(包括numbers, strings, 甚至是集合).

.. code-block:: lua

    >x = {} -- empty table
    >print(x)

更多table信息见后面

Functions:

如很多动态语言，函数可以赋值给变量

.. code-block:: lua

    >foo = function() print("hello") end
    >foo() -- call function
    >print(foo)

function也可以放入tables

.. code-block:: lua

    > a = "aeiou" -- a string
    > b = 13      -- a number
    > c = function()  -- a function
    >  print ("\n\n\tAin't it grand")
    > end
    > d = { a, b ,c} -- put them in a table
    > function printit(tata)  -- print their types.
    > table.unpack(tata) -- unpack the table
    > for key, value in ipairs(tata) do print(key, type(value)) end
    > end
    > printit(d)
    1       string
    2       number
    3       function

nil values:

.. code-block:: lua

    >print(x) --x is not defined before
    nil
    >t = nil
    >print(t)

Userdata:

Userdata变量是lua外部的对象，比如在C中实现的对象。

Thread:

一个thread代表独立的执行线程

Querying type:

lua是反射语言，可以通过type得到变量类型

.. code-block:: lua

    >x = '123'
    >print(x, type(x))

Tables
======================

.. code-block:: lua

    >t = {}
    >t['foo'] = 123
    >t[3] = 'bar'
    > = t[3] -- return t[3]
    >t[3] = nil -- earse a key/value
    >f = function() end
    >t[f] = 456 --任何值都可以作为key，除了nil和NAN(not a number)
    >t.bar = 789
    >= t['bar']

    --另一种添加key/value的方法
    > t = {["foo"] = "bar", [123] = 456}
    > = t.foo
    bar
    > = t[123]
    456

    --或者
    > t = {foo = "bar"} -- same as ["foo"]="bar" (but not [foo]="bar" , that would use the variable foo)
    > = t["foo"]
    bar

如同数组般使用tables

.. code-block:: lua

    > t = {"a", "b", "c"}
    > = t[1] -- 注意第一个index是1,不是0
    a
    > = t[3]
    c

    --混合模式
    > t = {"a", "b", [123]="foo", "c", name="bar", "d", "e"}
    > for k,v in pairs(t) do print(k,v) end
    1       a
    2       b
    3       c
    4       d
    5       e
    123     foo
    name    bar

    >t = {'a', 'b','c'}
    >= #t --数组t的长度
    3

    --add item to the end of array
    > t = {}
    > table.insert(t, 123)
    > t[#t+1] = 456
    > = t[1]
    123
    > = t[2]
    456

    --也可以指定位置insert
    > t = {"a", "c"}
    > table.insert(t, 2, "b")
    > = t[1], t[2], t[3]
    a b c

    --remove
    > t = {"a", "b", "c"}
    > table.remove(t, 2)
    > = t[1], t[2]
    a c

    --拼接
    > t = {"a", "b", "c"}
    > = table.concat(t, ";")
    a;b;c

table是引用类型，意识是赋值给其他变量时不会产生copy数据

.. code-block:: lua

    > t = {}
    > u = t
    > u.foo = "bar"
    > = t.foo
    bar
    > function f(x) x[1] = 2 end
    > f(t)
    > = u[1]
    2

许多新学习lua的喜欢把table当作数组使用，即使不需要顺序。但这样的问题是删除会很慢（需要移动其他item）检查一个item是否存在也很慢（需要轮寻全部item）

解决办法是把item存在key中，value设置一个dummy值（如true），你就可以像使用无序集合那样来使用table，快速的插入，删除和查找。

这样做的缺点是不好得到item总数（需要循环），也不能存储相同item两次

Functions
======================

lua中定义函数如下::

    function ( args ) body end

return value:

.. code-block:: lua

    > f = function ()
    >>  return "x", "y", "z" -- return 3 values
    >> end
    > a, b, c, d = f() -- assign the 3 values to 4 variables. the 4th variable will be filled with nil
    > = a, b, c, d
    x y z nil
    > a, b = (f()) -- wrapping a function call in () discards multiple return values
    > = a, b
    x, nil
    > = "w"..f() -- using a function call as a sub-expression discards multiple returns
    wx
    > print(f(), "w") -- same when used as the arg for another function call...
    x w
    > print("w", f()) -- ...except when it's the last arg
    w x y z
    > print("w", (f())) -- wrapping in () also works here like it does with =
    w x
    > t = {f()} -- multiple returns can be stored in a table
    > = t[1], t[2], t[3]
    x y z

参数个数可变:

.. code-block:: lua

    > f = function (x, ...)
    >>  x(...)
    >> end
    > f(print, 1,2,3)
    1 2 3

    > f=function(...) print(select("#", ...)) print(select(3, ...)) end
    > f(1, 2, 3, 4, 5)
    5
    3 4 5

named function:

.. code-block:: lua

    >function f(...) end -- equivalent to 
    >f = function(...) end 

tail calls:

.. code-block:: lua

    function factorial_helper(i, acc)
      if i == 0 then
        return acc
      end
      return factorial_helper(i-1, acc*i)
    end
    
    function factorial(x)
      return factorial_helper(x, 1)
    end

Thread
====================

lua的thread其实是协程

yielding:

.. code-block:: lua

    > function foo()
    >>   print("foo", 1)
    >>   coroutine.yield()
    >>   print("foo", 2)
    >> end
    >
using coroutine.create(fn) to create a coroutine

.. code-block:: lua

    > co = coroutine.create(foo) -- create a coroutine with foo as the entry
    > = type(co)                 -- display the type of object "co"
    thread

thread state:

.. code-block:: lua

    > = coroutine.status(co)
    suspended --The state suspended means that the thread is alive, and as you would expect, not doing anything.

use coroutine.resume() to start the thread, lua will enter the thread and leave when the thread yields

.. code-block:: lua

    > = coroutine.resume(co)
    foo     1
    true
    > = coroutine.resume(co)
    foo     2
    true
    > = coroutine.status(co)
    dead
    > = coroutine.resume(co)
    false   cannot resume dead coroutine
