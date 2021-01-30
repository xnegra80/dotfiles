alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='exa --icons'
alias vim='nvim'
alias emacs='devour emacs'

export VISUAL=emacs
export EDITOR="$VISUAL"
set -U fish_user_paths $HOME/.emacs.d/bin $fish_user_paths

if status is-interactive
   pfetch
   abbr --add --global yc 'yay -Yc'
   abbr --add --global yu 'yay -Syu'
   abbr --add --global df 'dotfiles'
   abbr --add --global v 'vim'
   abbr --add --global e 'emacs'
   abbr --add --global s 'systemctl'
   abbr --add --global gcco 'gcc -g -Wall -Wextra -o'
   abbr --add --global gccc 'gcc -g -Wall -Wextra -c'
end
starship init fish | source

thefuck --alias | source
