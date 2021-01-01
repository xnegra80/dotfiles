call plug#begin('~/.config/nvim/autoload/plugged')
    " Dracula colour scheme
    Plug 'dracula/vim', { 'as': 'dracula' }
    " Better Syntax Support
    Plug 'sheerun/vim-polyglot'
    " Intellisense
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    " Statusline
    Plug 'vim-airline/vim-airline'
    " Session Manager
    Plug 'mhinz/vim-startify'
    " Snipper
    Plug 'unblevable/quick-scope'
    " Commenter
    Plug 'tpope/vim-commentary'
    " Git
    Plug 'mhinz/vim-signify'
    Plug 'tpope/vim-fugitive'
    Plug 'tpope/vim-rhubarb'
    Plug 'junegunn/gv.vim'
    " Global search
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'
    Plug 'airblade/vim-rooter'
    " Colorizer of hex
    Plug 'norcalli/nvim-colorizer.lua'
    " Icons
    Plug 'ryanoasis/vim-devicons'
    " File Explorer
    Plug 'preservim/nerdtree'
    Plug 'Xuyuanp/nerdtree-git-plugin'
    "
    Plug 'liuchengxu/vim-which-key'
    Plug 'jiangmiao/auto-pairs'
    Plug 'vimwiki/vimwiki'

call plug#end()
