" Map leader to which_key
nnoremap <silent> <leader> :silent WhichKey '<Space>'<CR>
vnoremap <silent> <leader> :silent <c-u> :silent WhichKeyVisual '<Space>'<CR>

" Create map to add keys to
let g:which_key_map =  {}
let g:which_key_map.g =  {'name': '+git'}
" Define a separator
let g:which_key_sep = '→'
set timeoutlen=100


" Not a fan of floating windows for this
let g:which_key_use_floating_win = 1

" Change the colors if you want
highlight default link WhichKey          Operator
highlight default link WhichKeySeperator DiffAdded
highlight default link WhichKeyGroup     Identifier
highlight default link WhichKeyDesc      Function

" Hide status line
autocmd! FileType which_key
autocmd  FileType which_key set laststatus=0 noshowmode noruler
  \| autocmd BufLeave <buffer> set laststatus=2 noshowmode ruler

let g:which_key_map['h'] = [ '<C-W>s', 'split below']
let g:which_key_map['o'] = [ ':Startify', 'start screen' ]
let g:which_key_map['v'] = [ '<C-W>v', 'split right']

let g:which_key_map.g['j'] = ['<plug>(signify-next-hunk)', 'next change']
let g:which_key_map.g['k'] = ['<plug>(signify-prev-hunk)', 'previous change']
let g:which_key_map.g['s'] = [':G', 'status']
let g:which_key_map.g['f'] = [':diffget //2', 'accept left']
let g:which_key_map.g['h'] = [':diffget //3', 'accept right']


" Register which key map
call which_key#register('<Space>', "g:which_key_map")
