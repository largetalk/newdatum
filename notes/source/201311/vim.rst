=======================
vim整理
=======================

以前也写过一些vim的博客，如 http://blog.csdn.net/largetalk/article/details/8259813 和 http://blog.csdn.net/largetalk/article/details/6976721

这两天接触了一下ag和jedi, 非常好用，就把新的使用和以前的一起整理一下

vimpyre
====================

vim插件管理利器 ::

    sudo apt-get install vimpyre 或 pip install vimpyre #安装
    vimpyre init
    vimpyre search ag #搜索
    vimpyre install ag #安装ag
    vimpyre list_installed

vundle
====================

另一个vim插件管理，也是我现在用的

安装 ::

    git clone http://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

然后将下列代码加入vimrc中即可. (插件名字由git repo决定, 可以在http://vim-scripts.org/vim/scripts.html页面中查找) ::

    set nocompatible    " be iMproved
    filetype off        " required!
    
    set rtp+=~/.vim/bundle/vundle/
    call vundle#rc()
    
    " let Vundle manage Vundle
    " required!
    Bundle 'gmarik/vundle'
    
    " vim-scripts repos
    Bundle 'vim-plugin-foo'
    Bundle 'vim-plugin-bar'
    
    filetype plugin indent on    " required!

然后 ::

    :BundleInstall  #安装插件
    :BundleInstall! #更新插件
    :BundleClean    #卸载不在列表中的插件

常用插件
======================

这些只是我常用的插件

ag.vim
---------------------

https://github.com/rking/ag.vim

The Silver Searcher的vim前端插件， 安装ag之前先安装The Silver Searcher ::

    git clone https://github.com/ggreer/the_silver_searcher ag && cd ag && ./build.sh && sudo make install

然后把下句放入.vimrc ::

    let g:agprg="<custom-ag-path-goes-here> --column"

使用 ::

    :Ag [options] {pattern} [{directory}]

nerdtree 
-------------------

https://github.com/scrooloose/nerdtree.git

树形展示文件目录, 添加下句到.vimrc方便使用 ::

    nnoremap f :NERDTreeToggle 

dwm.vim 
--------------------

https://github.com/spolu/dwm.vim.git

窗口管理, 使用 ::

    - `C-N` Creates a new window and place it in the master pane [M] & stacks all previous windows in the stacked pane [S]
    - `C-C` Close the current window if no unsaved changes
    - `C-J` Jumps to next window (clockwise)
    - `C-K` Jumps to previous window (anti-clockwise)
    - `C-Space` Focus the current window, that is, place it in the master pane [M] & stacks all other windows in the stacked pane [S]
    - `C-M` Fullscreen mode for the current window (use focus to return to normal mode)

Pydiction 
----------------

https://github.com/vim-scripts/Pydiction.git

jedi-vim 
-----------------

https://github.com/davidhalter/jedi-vim.git

python自动补全，比pythoncomplete好用, 使用 ::

    Completion <C-Space>
    Goto assignments <leader>g (typical goto function)
    Goto definitions <leader>d (follow identifier as far as possible, includes imports and statements)
    Show Documentation/Pydoc K (shows a popup with assignments)
    Renaming <leader>r
    Usages <leader>n (shows all the usages of a name)
    Open module, e.g. :Pyimport os (opens the os module)

其实用<leader> 默认是 '\'

pyfold 
-------------------

https://github.com/vim-scripts/pyfold.git

vimim 
--------------------

https://github.com/vimim/vimim.git

中文输入，以前使用ibus输入法的时候由于不能在终端输入中文所以常使用, 后来使用fcitx就不怎么使用了


pyflakes 
---------------------

https://github.com/vim-scripts/pyflakes.git

python语法检查插件

快捷键
========================

::

    移动光标类命令  
    w或W ：光标右移一个字至字首  
    b或B ：光标左移一个字至字首  
    e或E ：光标右移一个字至字尾  
    ) ：光标移至句尾  
    ( ：光标移至句首  
    }：光标移至段落开头  
    {：光标移至段落结尾  
    nG：光标移至第n行首  
    n+：光标下移n行  
    n-：光标上移n行  
    n$：光标下移n-1行， 并到行尾  
    H ：光标移至屏幕顶行  
    M ：光标移至屏幕中间行  
    L ：光标移至屏幕最后行  
      
      
    屏幕翻滚类命令  
    Ctrl+u：向文件首翻半屏  
    <del>Ctrl+d：向文件尾翻半屏</del>  (已被我键绑定到 :q)  
    Ctrl+f：向文件尾翻一屏  
    Ctrl＋b；向文件首翻一屏  
    nzz：将第n行滚至屏幕中部，不指定n时将当前行滚至屏幕中部。  
      
    插入文本类命令  
    I ：在当前行首  
    A：在当前行尾  
    o：在当前行之下新开一行  
    O：在当前行之上新开一行  
    R：替换当前字符及其后的字符，直至按ESC键  
    s：从当前光标位置处开始，以输入的文本替代指定数目的字符  
    S：删除指定数目的行，并以所输入文本代替之  
    ncw或nCW：修改指定数目的字(word)  
    nC：修改指定数目的行  
      
    删除命令  
    ndw或ndW：删除光标处开始及其后的n-1个字(word)  
    d0：删至行首  
    d$：删至行尾  
    x或X：删除一个字符，x删除光标后的，而X删除光标前的  
    Ctrl+u：插入模式下， 删除上一行  
      
    搜索及替换命令  
    /pattern：从光标开始处向文件尾搜索pattern  
    ?pattern：从光标开始处向文件首搜索pattern  
    n：在同一方向重复上一次搜索命令  
    N：在反方向上重复上一次搜索命令  
    ：s/p1/p2/g：将当前行中所有p1均用p2替代  
    ：n1,n2s/p1/p2/g：将第n1至n2行中所有p1均用p2替代  
      
      
    选项设置  
    all：列出所有选项设置情况  
    term：设置终端类型  
    ignorecase：在搜索中忽略大小写  
    list：显示制表位(Ctrl+I)和行尾标志（$)  
    number：显示行号  
    report：显示由面向行的命令修改过的数目  
    terse：显示简短的警告信息  
    warn：在转到别的文件时若没保存当前文件则显示NO write信息  
    nomagic：允许在搜索模式中，使用前面不带“\”的特殊字符  
    nowrapscan：禁止vi在搜索到达文件两端时，又从另一端开始  
    mesg：允许vi显示其他用户用write写到自己终端上的信息  
      
    最后行方式命令  
    ：e filename：打开文件filename进行编辑  
    ：x：保存当前文件并退出  
    ：!command：执行shell命令command  
    ：n1,n2 w!command：将文件中n1行至n2行的内容作为command的输入并执行之，若不指定n1，n2，则表示将整个文件内容作为command的输入  
    ：r!command：将命令command的输出结果放到当前行  

