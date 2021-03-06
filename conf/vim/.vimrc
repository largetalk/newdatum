call pathogen#runtime_append_all_bundles("vimpyre")

let Tlist_Ctags_Cmd='/usr/bin/ctags'
set nocompatible
set cc=89
filetype plugin indent on
autocmd FileType python setlocal et sta sw=4 sts=4
set background=dark
autocmd BufRead,BufNewFile *.py syntax on
autocmd BufRead,BufNewFile *.py set ai
set tags=./tags,./../tags;
set autochdir
set shellslash
set grepprg=grep\ -nH\ $*
set fillchars=vert:\ ,stl:\ ,stlnc:\
highlight StatusLine guifg=SlateBlue guibg=Yellow
highlight StatusLineNC guifg=Gray guibg=White
"hi PmenuSel ctermfg=white ctermbg=darkmagenta guifg=white guibg=darkmagenta
set ww=h,l,<,>,[,],b,s " move over new lines
set hls
set ch=2 " enlarge cmdheight so as to avoid the message "HIT ENTER TO CONTINUE"
colorscheme elflord "murphy
map <Space> ^F " spacebar in command mode to pagedown
map <BS> X
map <Up> gk
map <Down> gj
map <C-D> :q<CR>
noremap <F5> <ESC>:w<CR> \| :! python %<CR>
noremap <F3> <ESC>:w<CR> \| :! pdflatex %<CR>
noremap <F8> <ESC>:pyf ~/tree.py<CR> 
"noremap <F2> <ESC>:w<CR> \| :silent! execute '!firefox http://jerrynb/doc/php-docs-20071125-r2/en/html/function.'.  substitute(expand('<cword>'),'_','-','g') .'.html'<CR>

vnoremap <Leader>p p
vnoremap p "_dP
set number
set showmatch
set ignorecase
set autoindent
set mps+=<:>
"set mouse=a
set tabstop=4
set shiftwidth=4
set softtabstop=4
set modeline
set smartcase
set wrap
set linebreak
set nolist
"set textwidth=72
set diffopt=filler,context:3
set backupdir=~/.vimbackup//
set directory=~/.vimswp//
set formatoptions=ctroqwn
set ruler
set rulerformat=%20(%2*%<%f%=\ %m%r\ %3l\ %c\ %p%%%)
set expandtab
"set wildmode=list:full
set clipboard+=unnamed 

set fdm=marker
fun! MyIndent(lnum)
	let s:sw = &shiftwidth
	if getline(a:lnum) =~ '\s*{$'
		return indent(a:lnum) + s:sw
	elseif getline(a:lnum) =~ '\s*}$'
		return indent(a:lnum) - s:sw
	else
		return indent(a:lnum)
endf


augroup JumpCursorOnEdit
  au!
  autocmd BufReadPost *
    \   if line("'\"") > 1 && line("'\"") <= line("$") |
    \     let JumpCursorOnEdit_foo = line("'\"") |
    \     let b:doopenfold = 1 |
    \     if (foldlevel(JumpCursorOnEdit_foo) > foldlevel(JumpCursorOnEdit_foo - 1)) |
    \        let JumpCursorOnEdit_foo = JumpCursorOnEdit_foo - 1 |
    \        let b:doopenfold = 2 |
    \     endif |
    \     exe JumpCursorOnEdit_foo |        
    \     exe "normal! g`\"" |
    \   endif |
  " Need to postpone using "zv" until after reading the modelines.
  autocmd BufWinEnter *
    \ if exists("b:doopenfold") |
    \   exe "normal zv" |
    \   if(b:doopenfold > 1) |
    \       exe  "+".1 |
    \   endif |
    \   unlet b:doopenfold |
    \ endif
augroup END 

let html_use_css = 0
let html_output_xhtml = 1
let html_whole_filler=1
let use_xhtml = 1
let html_use_encoding = 'utf-8'

nmap <leader>bl :Tlist<CR>

set wildmenu
autocmd FileType ruby,eruby set omnifunc=rubycomplete#Complete
"autocmd FileType python set omnifunc=pythoncomplete#Complete
autocmd FileType javascript set omnifunc=javascriptcomplete#CompleteJS
autocmd FileType html set omnifunc=htmlcomplete#CompleteTags
autocmd FileType css set omnifunc=csscomplete#CompleteCSS
autocmd FileType php set omnifunc=phpcomplete#CompletePHP

if $TERM =~ "-256color"
  set t_Co=256
  colorscheme ee
endif

" 能够漂亮地显示.NFO文件
set encoding=utf-8
function! SetFileEncodings(encodings)
let b:myfileencodingsbak=&fileencodings
let &fileencodings=a:encodings
endfunction
function! RestoreFileEncodings()
let &fileencodings=b:myfileencodingsbak
unlet b:myfileencodingsbak
endfunction

au BufReadPre *.nfo call SetFileEncodings('cp437')|set ambiwidth=single
au BufReadPost *.nfo call RestoreFileEncodings()

function AddTitle()
call append(0,"/************************************************************************")
call append(1,"*    Author: Arthur - largetalk@gmail.com")
call append(2,"*    "."Last modified: " . strftime("%Y-%m-%d %H:%M"))
call append(3,"*    Filename: " . expand("%"))
call append(4,"*    Description: ")
call append(5,"*************************************************************************/")
endf
 
function AddNotes()
call setline(line("."),"/*******************************************************************")
call append(line("."),"* Description: ")
call append(line(".")+1,"********************************************************************/    ")
endf

"NERD Tree
let NERDTreeIgnore=['\.pyc$']
let NERDChristmasTree=1
let NERDTreeAutoCenter=1
let NERDTreeBookmarksFile=$VIM.'\Data\NerdBookmarks.txt'
let NERDTreeMouseMode=2
let NERDTreeShowBookmarks=1
let NERDTreeShowFiles=1
"let NERDTreeShowHidden=1
"let NERDTreeShowLineNumbers=1
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
nnoremap f :NERDTreeToggle

" for chinese 
let &termencoding=&encoding
set fileencodings=utf-8,gbk,ucs-bom,cp936

"for grep.vim
let Grep_Skip_Dirs='.svn RCS CVS log SCCS'
let  Grep_Skip_Files='*.bak *~ *.pyc *.svn-base' 

"for pydiction
"let g:pydiction_location = '~/.vim/vimpyre/Pydiction/complete-dict'
"syntax enable
"set foldmethod=indent

"for jedi-vim
let g:jedi#popup_select_first = 0
let g:jedi#goto_assignments_command = "<leader>g"
let g:jedi#goto_definitions_command = "<leader>d"
let g:jedi#documentation_command = "K"
let g:jedi#usages_command = "<leader>n"
let g:jedi#completions_command = "<C-Space>"
let g:jedi#rename_command = "<leader>r"
let g:jedi#show_call_signatures = "1"

"for ag.vim
let g:agprg="/usr/local/bin/ag --column"
