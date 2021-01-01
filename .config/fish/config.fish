alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='exa --icons'
alias vim='nvim'

export VISUAL=emacs
export EDITOR="$VISUAL"
set -U fish_user_paths $HOME/.emacs.d/bin $fish_user_paths

if status is-interactive
   pfetch
end
starship init fish | source

thefuck --alias | source
