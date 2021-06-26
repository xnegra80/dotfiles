if status is-interactive
   paleofetch
end

fish_vi_key_bindings
bind -M insert -m default jk backward-char force-repaint
bind " " expand-abbr or self-insert

alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias ls='colorls --dark'
alias cat='bat --theme=Dracula --style=plain'
alias emacs='devour emacsclient -c'

abbr --add --global p 'paru'
abbr --add --global pc 'paru -c'
abbr --add --global df 'dotfiles'
abbr --add --global v 'vim'
abbr --add --global e 'emacs'
abbr --add --global se 'emacs /doas::/'
abbr --add --global et 'emacsclient -t'
abbr --add --global s 'systemctl'
abbr --add --global gcco 'gcc -g -Wall -Wextra -o'
abbr --add --global gccc 'gcc -g -Wall -Wextra -c'

export GEM_HOME=(ruby -e 'puts Gem.user_dir')

starship init fish | source

thefuck --alias | source
