========================
Linux安装字体
========================

ubuntu桌面版直接点击字体文件就可以安装, 手动安装方式需要，

在/usr/share/fonts/目录下，新建一个文件夹。比如，我安装consolas字体，就新建了一个名为consolas的文件夹。

然后执行如下步骤::

    sudo mkdir /usr/share/fonts/consolas
    sudo cp consolas.ttf  /usr/share/fonts/consolas
    sudo chmod 644 /usr/share/fonts/consolas/*
    cd /usr/share/fonts/consolas
    sudo mkfontscale
    sudo mkfontdir
    sudo fc-cache -fv

