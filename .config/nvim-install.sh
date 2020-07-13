#!/bin/bash

XTRACE=$(set +o | grep xtrace)
set -o xtrace

echo "Install Neovim"
brew install nvim

echo "Install yarn"
brew install yarn

echo "Install Vim-plug as Package Manager"
curl -fLo ~/.config/nvim/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim

echo "Get init.vim"
cp -rf ~/dotfiles/.config/nvim/ ~/.config/nvim

echo "Install vim plugins"
nvim --headless +PlugInstall +qall
brew install ripgrep

echo "Install coc extensions"
cp -rf ~/dotfiles/.config/coc/ ~/.config/coc
cd ~/.config/coc/extensions/
yarn install

$XTRACE
