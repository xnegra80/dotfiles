;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets.
(setq user-full-name "Gordon Lee"
      user-mail-address "hkgordonlee@gmail.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom. Here
;; are the three important ones:
;;
;; + `doom-font'
;; + `doom-variable-pitch-font'
;; + `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;;
;; They all accept either a font-spec, font string ("Input Mono-12"), or xlfd
;; font string. You generally only need these two:
(setq doom-font (font-spec :family "VictorMono Nerd Font" :size 15)
      doom-variable-pitch-font (font-spec :family "VictorMono Nerd Font" :size 15)
      doom-big-font (font-spec :family "VictorMono Nerd Font" :size 24)
      doom-variable-pitch-font (font-spec :family "SourceCodePro")
      doom-serif-font (font-spec :family "SourceCodePro")
      doom-unicode-font (font-spec :family "Font Awesome 5 Pro")
)

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-dracula)
(setq org-fancy-priorities-list '("" "" "☕" ""))
;; Connect to main workspace on incomming emacsclient session
(after! persp-mode
  (setq persp-emacsclient-init-frame-behaviour-override "main"))

;; whitespace
;; (remove-hook 'after-change-major-mode-hook #'doom-highlight-non-default-indentation-h)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/x/notes/")
(setq org-hide-emphasis-markers t)

(setq treemacs-position 'right)

;; (after! before-save-hook
;;   (setq highlight-indent-guides-mode 'nil)
;;   (setq highlight-indent-guides-mode 1))

(defun org-checkbox-todo ()
  "Switch header TODO state to DONE when all checkboxes are ticked, to TODO otherwise"
  (let ((todo-state (org-get-todo-state)) beg end)
    (unless (not todo-state)
      (save-excursion
    (org-back-to-heading t)
    (setq beg (point))
    (end-of-line)
    (setq end (point))
    (goto-char beg)
    (if (re-search-forward "\\[\\([0-9]*%\\)\\]\\|\\[\\([0-9]*\\)/\\([0-9]*\\)\\]"
                   end t)
        (if (match-end 1)
        (if (equal (match-string 1) "100%")
            (unless (string-equal todo-state "DONE")
              (org-todo 'done))
          (unless (string-equal todo-state "TODO")
            (org-todo 'todo)))
          (if (and (> (match-end 2) (match-beginning 2))
               (equal (match-string 2) (match-string 3)))
          (unless (string-equal todo-state "DONE")
            (org-todo 'done))
        (unless (string-equal todo-state "TODO")
          (org-todo 'todo)))))))))
(add-hook 'org-checkbox-statistics-hook 'org-checkbox-todo)

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type t)
(setq scroll-step 1)
(setq scroll-margin 1)
(setq mouse-wheel-scroll-amount '(1 ((shift) . 1))) ;; one line at a time
(setq mouse-wheel-progressive-speed nil) ;; don't accelerate scrolling
(setq mouse-wheel-follow-mouse 't) ;; scroll window under mouse
;; Here are some additional functions/macros that could help you configure Doom:
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
(defun comment-or-uncomment-line-or-region ()
  "Toggles commenting on the current line if no region is defined,
   otherwise toggles comments on the region"
  (interactive "*")
  (let ((use-empty-active-region t) (mark-even-if-inactive nil))
    (cond
     ((use-region-p) (comment-or-uncomment-region (region-beginning) (region-end)))
     (t (comment-or-uncomment-region (line-beginning-position) (line-end-position))))));
(map! "C-/" #'comment-or-uncomment-line-or-region )

(after! ispell
  ;; Don't spellcheck org blocks
  (pushnew! ispell-skip-region-alist
            '(":\\(PROPERTIES\\|LOGBOOK\\):" . ":END:")
            '("#\\+BEGIN_SRC" . "#\\+END_SRC")
            '("#\\+BEGIN_EXAMPLE" . "#\\+END_EXAMPLE"))

  )

(setq projectile-project-search-path '"~/dev/")
(setq projectile-sort-order 'modification-time)
(setq projectile-enable-caching t)
(setq projectile-file-exists-remote-cache-expire (* 10 60))
(setq projectile-require-project-root nil)

(setq lsp-pyright-typechecking-mode 'off)
(setq vterm-module-cmake-args "-DUSE_SYSTEM_LIBVTERM=yes")

(setq all-the-icons-scale-factor 1.1)
(after! doom-modeline
  (doom-modeline-def-modeline 'main
    '(bar matches buffer-info remote-host buffer-position parrot selection-info)
    '(misc-info minor-modes checker input-method buffer-encoding major-mode process vcs "  "))) ; <-- added padding here;; to get information about any of these functions/macros, move the cursor over

(use-package! doas-edit
  :if (executable-find "doas")
  :commands doas-edit-find-file doas-edit
  :init
  (map!
    [remap doom/sudo-find-file] #'doas-edit-find-file
    [remap doom/sudo-this-file] #'doas-edit))

(setq +workspaces-on-switch-project-behavior 'nil)

(require 'elcord)
;; (elcord-mode)

(require 'org-wild-notifier)
(org-wild-notifier-mode)
(setq alert-default-style 'libnotify)
(setq elcord-use-major-mode-as-main-icon 't)

;; (defun maybe-delete-frame-buffer (frame)
;;   "When a dedicated FRAME is deleted, also kill its buffer.
;; A dedicated frame contains a single window whose buffer is not
;; displayed anywhere else."
;;   (let ((windows (window-list frame)))
;;     (when (eq 1 (length windows))
;;       (let ((buffer (window-buffer (car windows))))
;;         (when (eq 1 (length (get-buffer-window-list buffer nil t)))
;;           (kill-buffer buffer))))))

;; (add-to-list 'delete-frame-functions #'maybe-delete-frame-buffer)



;; (custom-set-faces!
;;   '(mode-line :family "Noto Sans" :height 0.9)
;;   '(mode-line-inactive :family "Noto Sans" :height 0.9))
;; the highlighted symbol at press 'k' (non-evil users must press 'c-c c k').
;; This will open documentation for it, including demos of how they are used.
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.
