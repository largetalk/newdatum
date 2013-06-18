==============
 SVN 相关问题
==============

cannot set LC_CTYPE locale
==========================

在部分 server 上, 使用 svn update 命令时 会提示 cannot set LC_CTYPE locale .

症状:

.. code-block:: sh

    adaptive@mark:~$ svn up

    svn: warning: cannot set LC_CTYPE locale   

    svn: warning: environment variable LANG is en_US.UTF-8  

    svn: warning: please check that your locale name is correct   


解决方案:

.. code-block:: sh

   adaptive@mark:~$ export LC_ALL=C


编辑 `/etc/profile` 加入 上面的 export 命令到末尾, 使得下次开机时能够自动加入环境变量.


