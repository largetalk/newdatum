====================
Zero-sized Array
====================

在memcached源码中看到的:

.. code-block:: c

  /**
   * Structure for storing items within memcached.
   */
  typedef struct _stritem {
      ......
      /* this odd type prevents type-punning issues when we do
       * the little shuffle to save space when not using CAS. */
      union {
          uint64_t cas;
          char end;
      } data[];
      /* if it_flags & ITEM_CAS we have 8 bytes CAS */
      /* then null-terminated key */
      /* then " flags length\r\n" (no terminating null) */
      /* then data with terminating \r\n (no terminating null; it's binary!) */
  } item;

以前没有见过，而且用sizeof看，data字段完全不占空间，网上搜了下，做点笔记。

先看个例子,

.. code-block:: c

  #include <stdio.h>
  
  int main() {
      int arr[0];
      return 0;
  }

这段代码用gcc是可以编译通过的，只有在加入 -pedantic 边缘选项后会警告::

  $ gcc -pedantic test.c -o t
  test.c: In function ‘main’:
  test.c:22:9: warning: ISO C forbids zero-size array ‘arr’ [-pedantic]
