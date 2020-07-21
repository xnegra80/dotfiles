alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='exa --icons'
alias yay='pikaur'
alias yayr='pikaur -Rsn (pikaur -Qdtq)'
alias yayu='pikaur -Syu'
if status is-interactive
   pfetch
end
starship init fish | source
