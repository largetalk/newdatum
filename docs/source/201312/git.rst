==================
git指令简单介绍
==================

平时用git都只会用到几个很简单的命令，pull, push, commit等，其实git还有不少命令，正好最近可能会被问到，所以搜索并简记之。

git fetch
=================

git fetch 相当于是从远程获取最新版本到本地，但不自动merge::

    git fetch origin master #取远程origin的master分支最新版本到origin/master分支上
    git log -p master..origin/master #diff
    git merge origin/master #merge

git pull 就是取远程最新病自动merge::

    git pull origin master


git describe
=================

显示带注释的tag::

    git tag -a v1 -m "version 1 release"
    git describe

git hooks
==================

hooks即钩子，在.git/hooks目录下，有一些文件，根据文件名可以猜测到某些步骤时会被执行到的钩子，应该是任何脚本语言都可以

git reset
==================

reset命令有3种方式：

git reset –mixed：此为默认方式，不带任何参数的git reset，即时这种方式，它回退到某个版本，只保留源码，回退commit和index信息

git reset –soft：回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可

git reset –hard：彻底回退到某个版本，本地的源码也会变为上一个版本的内容

git remote
==================

:: 

    git remote rm origin #删除远程仓库
    git remote add origin git@github.com:xxx/yyy.git  #添加远程仓库

git rebase
==================

和merge差不多吧，但不会出现合并节点，这个以前写过，在http://blog.csdn.net/largetalk/article/details/7423015

git rerere
=================

很少见的一个命令， 名字代表的是reuse record resolution, 字面意思是让git记住你的冲突解决方式，并在以后可能重用。see: http://git-scm.com/blog/2010/03/08/rerere.html

git revert
=================

git revert 是撤销某次提交，该提交之后的提交会被保留，revert本身也会有一个commit

