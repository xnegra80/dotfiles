alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='exa --icons'
alias yay='pikaur'
alias sudo='doas'
if status is-interactive
   pfetch
end
starship init fish | source
