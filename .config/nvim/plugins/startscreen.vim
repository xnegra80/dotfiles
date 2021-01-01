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
            \ { 'sd': '~/dev/spaceship/spaceship-domestic-api' },
            \ { 'i': '~/.config/nvim/init.vim' },
            \ { 'f': '~/.config/fish/config.fish' },
            \ { 'c': '~/.config/qtile/config.py' },
            \ ]

let g:startify_session_autoload = 1
let g:startify_session_delete_buffers = 1
let g:startify_change_to_vcs_root = 1
let g:startify_fortune_use_unicode = 1
let g:startify_session_persistence = 1
let g:startify_enable_special = 0
let g:startify_custom_header = [
      \' ____ _______        __  ___   _   _ ____  _____      _    ____   ____ _   _',
      \'| __ )_   _\ \      / / |_ _| | | | / ___|| ____|    / \  |  _ \ / ___| | | |',
      \'|  _ \ | |  \ \ /\ / /   | |  | | | \___ \|  _|     / _ \ | |_) | |   | |_| |',
      \'| |_) || |   \ V  V /    | |  | |_| |___) | |___   / ___ \|  _ <| |___|  _  |',
      \'|____/ |_|    \_/\_/    |___|  \___/|____/|_____| /_/   \_\_| \_\\____|_| |_|'
      \]
