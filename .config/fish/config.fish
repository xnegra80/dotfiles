alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='colorls --dark'
alias vim='nvim'
alias cat='bat --theme=Dracula --style=plain'
alias emacs='TERM=xterm-24bit emacsclient -t'

export VISUAL=emacs
export EDITOR="$VISUAL"
set -U fish_user_paths $HOME/.emacs.d/bin $fish_user_paths

if status is-interactive
   pfetch
   abbr --add --global p 'paru'
   abbr --add --global pc 'paru -c'
   abbr --add --global df 'dotfiles'
   abbr --add --global v 'vim'
   abbr --add --global e 'emacs'
   abbr --add --global s 'systemctl'
   abbr --add --global gcco 'gcc -g -Wall -Wextra -o'
   abbr --add --global gccc 'gcc -g -Wall -Wextra -c'
end
starship init fish | source

thefuck --alias | source
