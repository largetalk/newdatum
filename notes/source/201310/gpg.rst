==================
发布签名文件
==================

A机器执行::

    gpg --gen-key #产生密钥对
    gpg --export -a > you.pub #导出公钥
    scp you.pub xxx@B:~/  #拷贝到B机器

B机器执行::

    gpg --import you.pub #导入A的公钥，需要使用root用户
    gpg --list-key #查看是否导入成功

在A机器上::

    echo 'i love you' > letter #需要发布的文件
    gpg -a -b -s letter #会产生一个letter.asc的文件
    #把这两个文件拷贝到B机器上同一个目录

在B机器上::

    gpg --verify letter.asc #验证letter是否来自A，以及文件是否被修改


