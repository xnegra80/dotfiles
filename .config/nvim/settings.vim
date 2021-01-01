let g:mapleader = "\<Space>"

syntax enable                           " Enables syntax highlighing
set formatoptions-=cro                  " Stop newline continution of comments
set hidden                              " Required to keep multiple buffers open multiple buffers
set nowrap                              " Display long lines as just one line
set encoding=utf-8                      " The encoding displayed
set pumheight=10                        " Makes popup menu smaller
set fileencoding=utf-8                  " The encoding written to file
set ruler              	                " Show the cursor position all the time
set cmdheight=2                         " More space for displaying messages
set iskeyword-=_                      	" Separate words with underscores
set mouse=a                             " Enable your mouse
set splitbelow                          " Horizontal splits will automatically be below
set splitright                          " Vertical splits will automatically be to the right
set t_Co=256                            " Support 256 colors
set conceallevel=0                      " So that I can see `` in markdown files
set tabstop=2                           " Insert 2 spaces for a tab
set shiftwidth=2                        " Change the number of space characters inserted for indentation
set smarttab                            " Makes tabbing smarter will realize you have 2 vs 4
set expandtab                           " Converts tabs to spaces
set smartindent                         " Makes indenting smart
set autoindent                          " Good auto indent
set laststatus=0                        " Always display the status line
set number                              " Line numbers
set smartcase                           " Only care about casing when there is an uppercase letter
set ignorecase
set background=dark                     " tell vim what the background color looks like
set termguicolors
set nobackup                            " This is recommended by coc
set nowritebackup                       " This is recommended by coc
set updatetime=300                      " Faster completion
set timeoutlen=100                      " By default timeoutlen is 1000 ms
set formatoptions-=cro                  " Stop newline continution of comments
set colorcolumn=80                      " Adds vertical line at 80 characters
set noshowmode                          " Hides the --MODE--"
set clipboard=unnamedplus               " Copy paste between vim and everything else
set autochdir
set lazyredraw
set nocompatible
filetype plugin on
set diffopt+=vertical                   " Git diff tool
au! BufWritePost $MYVIMRC source %      " auto source when writing to init.vm alternatively you can run :source $MYVIMRC
autocmd Filetype php setlocal shiftwidth=4

" You can't stop me
cmap w!! w !sudo tee %

autocmd BufWritePre * %s/\s\+$//e
autocmd InsertEnter * norm zz

autocmd! InsertLeave *.ms,*.md,*.tex call SaveTmp()

function! SaveTmp()
  let extension = expand('%:e')
  if extension == "ms"
          execute "w! /tmp/temp.ms"
  elseif extension == "tex"
          execute "w! /tmp/temp.tex"
  elseif extension == "md"
          execute "w! /tmp/temp.md"
  endif
  call Compile()
endfunction

function! Compile()
        let extension = expand('%:e')
        if extension == "ms"
                execute "! groff -ms /tmp/temp.ms -T pdf > /tmp/op.pdf"
        elseif extension == "tex"
                execute "! pandoc -f latex -t latex /tmp/temp.tex -o /tmp/op.pdf"
        elseif extension == "md"
                execute "! pandoc /tmp/temp.md -s -o /tmp/op.pdf"
        endif
endfunction

function! Preview()
        :call SaveTmp()
        execute "! zathura /tmp/op.pdf &"
endfunction

function! Wipeout()
  " list of *all* buffer numbers
  let l:buffers = range(1, bufnr('$'))

  " what tab page are we in?
  let l:currentTab = tabpagenr()
  try
    " go through all tab pages
    let l:tab = 0
    while l:tab < tabpagenr('$')
      let l:tab += 1

      " go through all windows
      let l:win = 0
      while l:win < winnr('$')
        let l:win += 1
        " whatever buffer is in this window in this tab, remove it from
        " l:buffers list
        let l:thisbuf = winbufnr(l:win)
        call remove(l:buffers, index(l:buffers, l:thisbuf))
      endwhile
    endwhile

    " if there are any buffers left, delete them
    if len(l:buffers)
      execute 'bwipeout' join(l:buffers)
    endif
  finally
    " go back to our original tab page
    execute 'tabnext' l:currentTab
  endtry
endfunction
