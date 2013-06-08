
all:

cur_path=$(shell pwd)
install: all
	ln -sf $(cur_path)/conf/.gitconfig ~/.gitconfig
