
all: git dict tmux

cur_path=$(shell pwd)
git: 
	@echo "#######install global gitconfig##########"
	ln -sf $(cur_path)/conf/gitconfig ~/.gitconfig
	@echo

dict:
	@echo '##############install dict utility###############'
	sudo ln -sf $(cur_path)/utility/dict.py /usr/local/bin/dict
	@echo

tmux:
	@echo '########install tmux conf###############'
	ln -sf $(cur_path)/conf/tmux.conf ~/.tmux.conf
	@echo
