alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='exa --icons'
alias vim='nvim'
alias emacs='devour emacsclient -c'

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
