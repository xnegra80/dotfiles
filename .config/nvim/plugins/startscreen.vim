let g:startify_session_dir = '~/.config/nvim/sessions'

let g:startify_lists = [
          \ { 'type': 'files',     'header': ['   Files']            },
          \ { 'type': 'dir',       'header': ['   Current Directory '. getcwd()] },
          \ { 'type': 'sessions',  'header': ['   Sessions']       },
          \ { 'type': 'bookmarks', 'header': ['   Bookmarks']      },
          \ ]

let g:startify_bookmarks = [
            \ { 'sp': '~/dev/spaceship/spaceship-business-panel' },
            \ { 'sf': '~/dev/spaceship/spaceship-business-frontend' },
            \ { 'sa': '~/dev/spaceship/spaceship-api-dev' },
            \ { 'i': '~/.config/nvim/init.vim' },
            \ { 'f': '~/.config/fish/config.fish' },
            \ { 'q': '~/.config/qtile/config.py' },
            \ ]

let g:startify_session_autoload = 1
let g:startify_session_delete_buffers = 1
let g:startify_change_to_vcs_root = 1
let g:startify_fortune_use_unicode = 1
let g:startify_session_persistence = 1
let g:startify_enable_special = 0
let g:startify_custom_header = [
        \ ' ____  _            _      _     _                  __  __       _   _',
        \ '| __ )| | __ _  ___| | __ | |   (_)_   _____  ___  |  \/  | __ _| |_| |_ ___ _ __',
        \ '|  _ \| |/ _` |/ __| |/ / | |   | \ \ / / _ \/ __| | |\/| |/ _` | __| __/ _ \ "__|',
        \ '| |_) | | (_| | (__|   <  | |___| |\ V /  __/\__ \ | |  | | (_| | |_| ||  __/ |',
        \ '|____/|_|\__,_|\___|_|\_\ |_____|_| \_/ \___||___/ |_|  |_|\__,_|\__|\__\___|_|',
        \]
