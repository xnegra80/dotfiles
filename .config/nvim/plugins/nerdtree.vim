autocmd StdinReadPre * let s:std_in=1
let g:NERDTreeShowHidden=1
let g:NERDTreeWinPos = "right"
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
let g:NERDTreeDirArrowExpandable = ''
let g:NERDTreeDirArrowCollapsible = ''
