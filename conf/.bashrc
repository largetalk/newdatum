# ~/.bashrc: executed by bash(1) for non-login shells.
#
# This file is sourced by all *interactive* bash shells on startup,
# including some apparently interactive shells such as scp and rcp
# that can't tolerate any output.  So make sure this doesn't display
# anything or bad things will happen !


# Test for an interactive shell.  There is no need to set anything
# past this point for scp and rcp, and it's important to refrain from
# outputting anything in those cases.
if [[ $- != *i* ]] ; then
	# Shell is non-interactive.  Be done now!
	return
fi

# Bash won't get SIGWINCH if another process is in the foreground.
# Enable checkwinsize so that bash will check the terminal size when
# it regains control.  #65623
# http://cnswww.cns.cwru.edu/~chet/bash/FAQ (E11)
shopt -s checkwinsize

# Enable history appending instead of overwriting.  #139609
shopt -s histappend

# Change the window title of X terminals 
case ${TERM} in
	xterm*|rxvt*|Eterm|aterm|kterm|gnome*|interix)
		PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\007"'
		;;
	screen)
		PROMPT_COMMAND='echo -ne "\033_${USER}@${HOSTNAME%%.*}:${PWD/$HOME/~}\033\\"'
		;;
esac

use_color=false

# Set colorful PS1 only on colorful terminals.
# dircolors --print-database uses its own built-in database
# instead of using /etc/DIR_COLORS.  Try to use the external file
# first to take advantage of user additions.  Use internal bash
# globbing instead of external grep binary.
safe_term=${TERM//[^[:alnum:]]/?}   # sanitize TERM
match_lhs=""
[[ -f ~/.dir_colors   ]] && match_lhs="${match_lhs}$(<~/.dir_colors)"
[[ -f /etc/DIR_COLORS ]] && match_lhs="${match_lhs}$(</etc/DIR_COLORS)"
[[ -z ${match_lhs}    ]] \
	&& type -P dircolors >/dev/null \
	&& match_lhs=$(dircolors --print-database)
[[ $'\n'${match_lhs} == *$'\n'"TERM "${safe_term}* ]] && use_color=true

if ${use_color} ; then
	# Enable colors for ls, etc.  Prefer ~/.dir_colors #64489
	if type -P dircolors >/dev/null ; then
		if [[ -f ~/.dir_colors ]] ; then
			eval $(dircolors -b ~/.dir_colors)
		elif [[ -f /etc/DIR_COLORS ]] ; then
			eval $(dircolors -b /etc/DIR_COLORS)
		fi
	fi

	if [[ ${EUID} == 0 ]] ; then
		PS1='\[\033[01;31m\]\u@\h\[\033[01;34m\]: \w \$\[\033[00m\] '
	else
		PS1='\[\033[01;32m\]\u@\h\[\033[01;34m\]: \w \$\[\033[00m\] '
	fi

	alias ls='ls --color=auto'
	alias grep='grep --colour=auto'
else
	if [[ ${EUID} == 0 ]] ; then
		# show root@ when we don't have colors
		PS1='\u@\h:\W \$ '
	else
		PS1='\u@\h:\w \$ '
	fi
fi

# Try to keep environment pollution down, EPA loves us.
unset use_color safe_term match_lhs


CL="\[\e[0m\]"
GREEN="$CL\[\e[0;32m\]"
BGREEN="$CL\[\e[0;32;1m\]"
XORG="$CL\[\e[0;36m\]"
XRED="$CL\[\e[0;35m\]"
BRED="$CL\[\e[0;35;1m\]"
ORG="$CL\[\e[0;33m\]"
DARK_GRAY="$CL\[\e[1;30m\]"
CYAN="$CL\[\e[1;36m\]"
BLUE="$CL\[\e[1;34m\]"

PROMPT_COMMAND='echo -ne "\033]0;${USER}@${HOSTNAME}: ${PWD}\007"
NTTY=$(tty | cut -d"/" -f3-4)
LS=$(ls | wc -l)
LSA=$(ls -a | wc -l)

L1a="$BLUE[$BGREEN\u$GREEN@\h:$NTTY\s$BLUE]$BLUE"
L1b="$ORG\t$BLUE"
L1c="$BLUE<$BRED\w$BLUE>$BLUE"
L1d="($XRED$LS/$LSA$BLUE)$BLUE"
L2="$CYAN\\\$$CL"
export PS1="$L1a-$L1b-$L1c-$L1d-\n$L2 "
#export PS1="[\u@\h:$NTTY\s]-\t-<\w:$LS/$LSA>-\n\\$ "
history -a
'

# For colourful man pages (CLUG-Wiki style)
export LESS_TERMCAP_mb=$'\033[01;31m'
export LESS_TERMCAP_md=$'\033[01;31m'
export LESS_TERMCAP_me=$'\033[0m'
export LESS_TERMCAP_se=$'\033[0m'
export LESS_TERMCAP_so=$'\033[01;44;33m'
export LESS_TERMCAP_ue=$'\033[0m'
export LESS_TERMCAP_us=$'\033[01;32m'

export JAVA_HOME="/usr/lib/jvm/java-6-sun-1.6.0.22"
export GREP_OPTIONS='--color=auto'

alias cp="cp -i"
alias rm='rm -i'
#alias info='pinfo'
alias ll='ls -l'
alias lh='ls -lh'
alias la='ls -A'
alias l='ls -CF'
alias wget='wget -c'
alias cdellis='cd /var/www/ellis'
alias cdbingo='cd /var/www/bingo/bingo'
alias cdsvn='cd ~/SVN/'
alias cdlog='cd ~/SVN/log_analytics/trunk'
alias cdhadoop='cd ~/SVN/log_analytics/branches/hadoop'
#alias mv='mv -i'
#alias rm='mv -f --target-directory=/tmp/'

mount | fgrep '/mnt/tex' > /dev/null 2>&1
[ $? -eq 0 ] && export PATH=/media/cdrom0/2005/bin/i386-linux/:$PATH

export HISTTIMEFORMAT='%Y-%m-%d %H:%M:%S '
export HISTSIZE=10000
export HISTIGNORE="&:clear:exit"
export HISTCONTROL=ignoreboth:erasedups
shopt -s histappend
#[ "$TERM" == "xterm" ] && export PROMPT_COMMAND="$PROMPT_COMMAND; history -a; history -n; history -w"
export SHELL=bash
export STAGING=development
#export GNUSTEP_MAKEFILES=/usr/GNUstep/System/Library/Makefiles
[[ -s "$HOME/.rvm/scripts/rvm" ]] && . "$HOME/.rvm/scripts/rvm"  # This loads RVM into a shell session.
