if status is-interactive
   pfetch
end

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='colorls --dark'
alias paru='paru --bottomup'
alias cat='bat --theme=Dracula --style=plain'
alias emacs='devour emacsclient -c'

abbr --add --global p 'paru'
abbr --add --global psyu 'paru -Syu'
abbr --add --global pc 'paru -c'
abbr --add --global df 'dotfiles'
abbr --add --global bt 'bashtop'
abbr --add --global v 'vim'
abbr --add --global e 'emacs'
abbr --add --global et 'TERM=xterm-24bit emacsclient -t'
abbr --add --global s 'systemctl'
abbr --add --global gcco 'gcc -g -Wall -Wextra -o'
abbr --add --global gccc 'gcc -g -Wall -Wextra -c'

export VISUAL="emacsclient -c"
export EDITOR="$VISUAL"
set -U fish_user_paths $HOME/.emacs.d/bin $fish_user_paths

starship init fish | source

thefuck --alias | source
