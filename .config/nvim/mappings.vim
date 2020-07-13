" ctrl + jk to navigate omnicomplete
inoremap <expr> <c-j> ("\<c-n>")
inoremap <expr> <c-k> ("\<c-p>")

" alt + hjkl to resize splits
nnoremap <m-j>    :resize -2<cr>
nnoremap <m-k>    :resize +2<cr>
nnoremap <m-h>    :vertical resize -2<cr>
nnoremap <m-l>    :vertical resize +2<cr>

" j + k to escape
inoremap jk <esc>
inoremap kj <esc>

" Use ctrl + u for easy caps
inoremap <c-u> <esc>viwUi
nnoremap <c-u> viwU<esc>

" ctrl + tab in normal mode will move to next buffer
nnoremap <tab> :bnext<cr>
" ctrl + shift + tab to go back
nnoremap <s-tab> :bprevious<cr>

" ctrl + q to quit without saving
nnoremap <c-q> :bd!<cr>
inoremap <c-q> <esc>:bd!<cr>

" ctrl + p to search file
nnoremap <c-p> :GFiles --cached --others<cr>

" ctrl + f to search text
nnoremap <c-f> :RG<cr>

" ctrl + e to open file tree
nnoremap <c-e> :NERDTreeFind %<cr>

" ctrl + / to comment
vnoremap <c-_> :Commentary<cr>
nnoremap <c-_> :Commentary<cr>

" ctrl + s to save
nnoremap <c-s> :w<cr>
inoremap <c-s> <esc>:w<cr>
" <TAB>: completion.
inoremap <expr><tab> pumvisible() ? "\<c-n>" : "\<tab>"

" Better tabbing
vnoremap < <gv
vnoremap > >gv

" ctrl + hjkl to navigate splits
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" space + enter sources init.vim
nnoremap <leader><cr> :so $MYVIMRC<cr>

" shift + jk moves line up/down
vnoremap J :m '>+1'<CR>gv=gv
vnoremap K :m '<-2>'<CR>gv=gv

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" THE COC
" ctrl + space to trigger completion.
inoremap <silent><expr> <c-space> coc#refresh()
" Use `[g` and `]g` to navigate diagnostics
" Use `:CocDiagnostics` to get all diagnostics of current buffer in location list.
nmap <silent> [g <Plug>(coc-diagnostic-prev)
nmap <silent> ]g <Plug>(coc-diagnostic-next)

" GoTo code navigation.
nmap <silent> gd <Plug>(coc-definition)
nmap <silent> gy <Plug>(coc-type-definition)
nmap <silent> gi <Plug>(coc-implementation)
nmap <silent> gr <Plug>(coc-references)

" Use K to show documentation in preview window.
nnoremap <silent> K :call <SID>show_documentation()<CR>

" Symbol renaming.
nmap <leader>rn <Plug>(coc-rename)

" Formatting selected code.
xmap <leader>f  <Plug>(coc-format-selected)
nmap <leader>f  <Plug>(coc-format-selected)

" Applying codeAction to the selected region.
" Example: `<leader>aap` for current paragraph
xmap <leader>a  <Plug>(coc-codeaction-selected)
nmap <leader>a  <Plug>(coc-codeaction-selected)

" Remap keys for applying codeAction to the current buffer.
nmap <leader>ac  <Plug>(coc-codeaction)
" Apply AutoFix to problem on the current line.
nmap <leader>qf  <Plug>(coc-fix-current)

" Map function and class text objects
" NOTE: Requires 'textDocument.documentSymbol' support from the language server.
xmap if <Plug>(coc-funcobj-i)
omap if <Plug>(coc-funcobj-i)
xmap af <Plug>(coc-funcobj-a)
omap af <Plug>(coc-funcobj-a)
xmap ic <Plug>(coc-classobj-i)
omap ic <Plug>(coc-classobj-i)
xmap ac <Plug>(coc-classobj-a)
omap ac <Plug>(coc-classobj-a)

" Mappings for CoCList
" Show all diagnostics.
nnoremap <silent><nowait> <space>a  :<C-u>CocList diagnostics<cr>
" Manage extensions.
nnoremap <silent><nowait> <space>e  :<C-u>CocList extensions<cr>
" Show commands.
nnoremap <silent><nowait> <space>c  :<C-u>CocList commands<cr>
" Find symbol of current document.
nnoremap <silent><nowait> <space>o  :<C-u>CocList outline<cr>
" Search workspace symbols.
" nnoremap <silent><nowait> <space>s  :<C-u>CocList -I symbols<cr>
" Do default action for next item.
nnoremap <silent><nowait> <space>j  :<C-u>CocNext<CR>
" Do default action for previous item.
nnoremap <silent><nowait> <space>k  :<C-u>CocPrev<CR>
" Resume latest coc list.
nnoremap <silent><nowait> <space>p  :<C-u>CocListResume<CR>s
