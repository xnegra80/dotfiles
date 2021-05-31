import qualified Data.Map as M
import Data.Maybe (isJust)
import Data.MaybeLike (fromJust)
import Data.Monoid
import System.Exit
import XMonad
import XMonad.Actions.CopyWindow
import XMonad.Actions.CycleWS
import XMonad.Actions.MouseResize
import XMonad.Actions.Promote
import XMonad.Actions.RotSlaves
import XMonad.Actions.WindowGo
import XMonad.Actions.WithAll
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.ManageDocks
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.SetWMName
import XMonad.Layout.Accordion
import XMonad.Layout.BoringWindows hiding (Replace)
import XMonad.Layout.Decoration
import XMonad.Layout.GridVariants (Grid (Grid))
import qualified XMonad.Layout.LayoutModifier
import XMonad.Layout.LimitWindows
import XMonad.Layout.Magnifier
import XMonad.Layout.MultiToggle
import qualified XMonad.Layout.MultiToggle as MT (Toggle (..))
import XMonad.Layout.MultiToggle.Instances
import XMonad.Layout.NoBorders
import XMonad.Layout.Renamed
import XMonad.Layout.ResizableTile
import XMonad.Layout.ShowWName
import XMonad.Layout.Simplest
import XMonad.Layout.SimplestFloat
import XMonad.Layout.Spacing
import XMonad.Layout.SubLayouts
import XMonad.Layout.Tabbed
import XMonad.Layout.ThreeColumns
import XMonad.Layout.ToggleLayouts
import qualified XMonad.Layout.ToggleLayouts as T
import XMonad.Layout.WindowArranger
import qualified XMonad.StackSet as W
import XMonad.Util.EZConfig
import XMonad.Util.NamedScratchpad
import XMonad.Util.Run
import XMonad.Util.SpawnOnce

myTerminal :: String
myTerminal = "alacritty"

myFont :: String
myFont = "xft:DejaVu Sans Mono:regular:size=9:antialias=true:hinting=true"

-- Whether focus follows the mouse pointer.
myFocusFollowsMouse :: Bool
myFocusFollowsMouse = True

-- Whether clicking on a window to focus also passes the click to the window
myClickJustFocuses :: Bool
myClickJustFocuses = False

-- Width of the window border in pixels.
--
myBorderWidth :: Dimension
myBorderWidth = 2

-- modMask lets you specify which modkey you want to use. The default
-- is mod1Mask ("left alt").  You may also consider using mod3Mask
-- ("right alt"), which does not conflict with emacs keybindings. The
-- "windows key" is usually mod4Mask.
--
myModMask :: KeyMask
myModMask = mod1Mask

windowCount :: X (Maybe String)
windowCount = gets $ Just . show . length . W.integrate' . W.stack . W.workspace . W.current . windowset

-- myWorkspaces = [" 1 ", " 2 ", " 3 ", " 4 ", " 5 ", " 6 ", " 7 ", " 8 ", " 9 "]
myWorkspaces :: [String]
myWorkspaces =
  [ " <fn=1>\xf086</fn> ",
    " <fn=1>\xf0ac</fn> ",
    " <fn=1>\xf120</fn> ",
    " <fn=1>\xf387</fn> ",
    " <fn=1>\xf865</fn> ",
    " <fn=1>\xf073</fn> ",
    " <fn=1>\xf78a</fn> ",
    " <fn=2>\xf3f6</fn> ",
    " <fn=2>\xf17a</fn> "
  ]

clickable :: WorkspaceId -> String
clickable w = xmobarAction ("xmonadctl view\\\"" ++ w ++ "\\\"") "1" w

-- Border colors for unfocused and focused windows, respectively.
--
myNormalBorderColor :: String
myNormalBorderColor = "#44475a"

myFocusedBorderColor :: String
myFocusedBorderColor = "#bd93f9"

myScratchPads :: [NamedScratchpad]
myScratchPads =
  [ NS "spotify" spawnSpotify findSpotify manageSpotify,
    NS "ranger" spawnRanger findRanger manageRanger
  ]
  where
    spawnSpotify = "spotify"
    findSpotify = className =? "Spotify"
    manageSpotify = customFloating $ W.RationalRect l t w h
      where
        h = 0.9
        w = 0.9
        t = 0.95 - h
        l = 0.95 - w
    spawnRanger = myTerminal ++ " -t ranger -e ranger"
    findRanger = title =? "ranger"
    manageRanger = customFloating $ W.RationalRect l t w h
      where
        h = 0.9
        w = 0.9
        t = 0.95 - h
        l = 0.95 - w

myKeys :: [(String, X ())]
myKeys =
  -- Xmonad
  [ ("M-S-r", spawn "xmonad --recompile; pkill xmobar; xmonad --restart"), -- Recompiles xmonad
  -- ("M-S-r", spawn "xmonad --restart"), -- Restarts xmonad
  -- ("M-S-q", io exitSuccess), -- Quits xmonad

    -- Run Prompt
    ("M-d", spawn "dmenu_run -i -p \"Run: \""), -- Dmenu

    -- Other Dmenu Prompts
    -- In Xmonad and many tiling window managers, M-p is the default keybinding to
    -- launch dmenu_run, so I've decided to use M-p plus KEY for these dmenu scripts.
    ("M-d a", spawn "dm-sounds"), -- choose an ambient background
    ("M-d b", spawn "dm-setbg"), -- set a background
    ("M-d c", spawn "dm-colpick"), -- pick color from our scheme
    ("M-d e", spawn "dm-confedit"), -- edit config files
    ("M-d i", spawn "dm-maim"), -- screenshots (images)
    ("M-d k", spawn "dm-kill"), -- kill processes
    ("M-d m", spawn "dm-man"), -- manpages
    ("M-d o", spawn "dm-bookman"), -- qutebrowser bookmarks/history
    ("M-d p", spawn "passmenu"), -- passmenu
    ("M-d q", spawn "dm-logout"), -- logout menu
    ("M-d r", spawn "dm-reddit"), -- reddio (a reddit viewer)
    ("M-d s", spawn "dm-websearch"), -- search various search engines

    -- Useful programs to have a keybinding for launch
    ("M-<Return>", spawn myTerminal),
    ("M-M1-h", spawn (myTerminal ++ " -e htop")),
    -- Kill windows
    ("M-S-q", kill1), -- Kill the currently focused client
    -- ("M-S-a", killAll), -- Kill all windows on current workspace

    -- Workspaces
    ("M-.", nextScreen), -- Switch focus to next monitor
    ("M-,", prevScreen), -- Switch focus to prev monitor
    ("M-S-<KP_Add>", shiftTo Next nonNSP >> moveTo Next nonNSP), -- Shifts focused window to next ws
    ("M-S-<KP_Subtract>", shiftTo Prev nonNSP >> moveTo Prev nonNSP), -- Shifts focused window to prev ws

    -- Floating windows
    ("M-f", sendMessage (T.Toggle "floats")), -- Toggles my 'floats' layout
    ("M-t", withFocused $ windows . W.sink), -- Push floating window back to tile
    ("M-S-t", sinkAll), -- Push ALL floating windows to tile

    -- Increase/decrease spacing (gaps)
    ("C-M1-j", decWindowSpacing 4), -- Decrease window spacing
    ("C-M1-k", incWindowSpacing 4), -- Increase window spacing
    ("C-M1-h", decScreenSpacing 4), -- Decrease screen spacing
    ("C-M1-l", incScreenSpacing 4), -- Increase screen spacing

    -- Windows navigation
    ("M-m", windows W.focusMaster), -- Move focus to the master window
    ("M-j", windows W.focusDown), -- Move focus to the next window
    ("M-k", windows W.focusUp), -- Move focus to the prev window
    ("M-S-m", windows W.swapMaster), -- Swap the focused window and the master window
    ("M-S-j", windows W.swapDown), -- Swap focused window with next window
    ("M-S-k", windows W.swapUp), -- Swap focused window with prev window
    ("M-<Backspace>", promote), -- Moves focused window to master, others maintain order
    ("M-S-<Tab>", rotSlavesDown), -- Rotate all windows except master and keep focus in place
    ("M-C-<Tab>", rotAllDown), -- Rotate all the windows in the current stack

    -- Layouts
    ("M-<Tab>", sendMessage NextLayout), -- Switch to next layout
    ("M-<Space>", sendMessage (MT.Toggle NBFULL) >> sendMessage ToggleStruts), -- Toggles noborder/full

    -- Increase/decrease windows in the master pane or the stack
    ("M-S-<Up>", sendMessage (IncMasterN 1)), -- Increase # of clients master pane
    ("M-S-<Down>", sendMessage (IncMasterN (-1))), -- Decrease # of clients master pane
    ("M-C-<Up>", increaseLimit), -- Increase # of windows
    ("M-C-<Down>", decreaseLimit), -- Decrease # of windows

    -- Window resizing
    ("M-h", sendMessage Shrink), -- Shrink horiz window width
    ("M-l", sendMessage Expand), -- Expand horiz window width
    ("M-M1-j", sendMessage MirrorShrink), -- Shrink vert window width
    ("M-M1-k", sendMessage MirrorExpand), -- Expand vert window width

    -- Sublayouts
    -- This is used to push windows to tabbed sublayouts, or pull them out of it.
    ("M-C-h", sendMessage $ pullGroup L),
    ("M-C-l", sendMessage $ pullGroup R),
    ("M-C-k", sendMessage $ pullGroup U),
    ("M-C-j", sendMessage $ pullGroup D),
    ("M-C-m", withFocused (sendMessage . MergeAll)),
    -- , ("M-C-u", withFocused (sendMessage . UnMerge))
    ("M-C-/", withFocused (sendMessage . UnMergeAll)),
    ("M-C-.", onGroup W.focusUp'), -- Switch focus to next tab
    ("M-C-,", onGroup W.focusDown'), -- Switch focus to prev tab

    -- Scratchpads
    -- Toggle show/hide these programs.  They run on a hidden workspace.
    -- When you toggle them to show, it brings them to your current workspace.
    -- Toggle them to hide and it sends them back to hidden workspace (NSP).
    ("M-s s", namedScratchpadAction myScratchPads "spotify"),
    ("M-s e", namedScratchpadAction myScratchPads "ranger"),
    -- Set wallpaper with 'feh'. Type 'SUPER+F1' to launch sxiv in the wallpapers directory.
    -- Then in sxiv, type 'C-x w' to set the wallpaper that you choose.
    ("M-<F1>", spawn "sxiv -r -q -t -o ~/wallpapers/*"),
    ("M-<F2>", spawn "/bin/ls ~/wallpapers | shuf -n 1 | xargs xwallpaper --stretch"),
    --, ("M-<F2>", spawn "feh --randomize --bg-fill ~/wallpapers/*")

    -- Controls for mocp music player (SUPER-u followed by a key)
    ("M-u p", spawn "mocp --play"),
    ("M-u l", spawn "mocp --next"),
    ("M-u h", spawn "mocp --previous"),
    ("M-u <Space>", spawn "mocp --toggle-pause"),
    -- Emacs (CTRL-e followed by a key)
    -- , ("C-e e", spawn myEmacs)                 -- start emacs
    ("C-e e", spawn "emacsclient -c -e '(dashboard-refresh-buffer)'"), -- emacs dashboard
    ("C-e b", spawn "emacsclient -c -e '(ibuffer)'"), -- list buffers
    ("C-e d", spawn "emacsclient -c -e '(dired nil)'"), -- dired
    -- , ("C-e v", spawn (myEmacs ++ ("--eval '(vterm nil)'"))) -- vterm if on GNU Emacs
    ("C-e v", spawn "-emacsclient -c -e '(+vterm/here nil)'"), -- vterm if on Doom Emacs
    -- , ("C-e w", spawn (myEmacs ++ ("--eval '(eww \"distrotube.com\")'"))) -- eww browser if on GNU Emacs
    -- Multimedia Keys
    ("<XF86AudioPlay>", spawn (myTerminal ++ "mocp --play")),
    ("<XF86AudioPrev>", spawn (myTerminal ++ "mocp --previous")),
    ("<XF86AudioNext>", spawn (myTerminal ++ "mocp --next")),
    ("<XF86AudioMute>", spawn "amixer set Master toggle"),
    ("<XF86AudioLowerVolume>", spawn "amixer set Master 5%- unmute"),
    ("<XF86AudioRaiseVolume>", spawn "amixer set Master 5%+ unmute"),
    ("<XF86HomePage>", spawn "qutebrowser https://www.youtube.com/c/DistroTube"),
    ("<XF86Search>", spawn "dmsearch"),
    ("<XF86Mail>", runOrRaise "thunderbird" (resource =? "thunderbird")),
    ("<XF86Calculator>", runOrRaise "qalculate-gtk" (resource =? "qalculate-gtk")),
    ("<XF86Eject>", spawn "toggleeject"),
    ("<Print>", spawn "dmscrot")
  ]
  where
    -- The following lines are needed for named scratchpads.
    nonNSP = WSIs (return (\ws -> W.tag ws /= "NSP"))
    nonEmptyNonNSP = WSIs (return (\ws -> isJust (W.stack ws) && W.tag ws /= "NSP"))

------------------------------------------------------------------------
-- Mouse bindings: default actions bound to mouse events
--
myMouseBindings XConfig {XMonad.modMask = modm} =
  M.fromList
    -- mod-button1, Set the window to floating mode and move by dragging
    [ ( (modm, button1),
        \w ->
          focus w >> mouseMoveWindow w
            >> windows W.shiftMaster
      ),
      -- mod-button2, Raise the window to the top of the stack
      ((modm, button2), \w -> focus w >> windows W.shiftMaster),
      -- mod-button3, Set the window to floating mode and resize by dragging
      ( (modm, button3),
        \w ->
          focus w >> mouseResizeWindow w
            >> windows W.shiftMaster
      )
      -- you may also bind events to the mouse scroll wheel (button4 and button5)
    ]

-- Layouts

mySpacing :: Integer -> l a -> XMonad.Layout.LayoutModifier.ModifiedLayout Spacing l a
mySpacing i = spacingRaw False (Border i i i i) True (Border i i i i) True

tall =
  renamed [Replace "tall"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          limitWindows 12 $
            mySpacing 8 $
              ResizableTall 1 (3 / 100) (1 / 2) []

magnify =
  renamed [Replace "magnify"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          magnifier $
            limitWindows 12 $
              mySpacing 8 $
                ResizableTall 1 (3 / 100) (1 / 2) []

monocle =
  renamed [Replace "monocle"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          limitWindows 20 Full

floats =
  renamed [Replace "floats"] $
    smartBorders $
      limitWindows 20 simplestFloat

grid =
  renamed [Replace "grid"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          limitWindows 12 $
            mySpacing 8 $
              mkToggle (single MIRROR) $
                Grid (16 / 10)

threeCol =
  renamed [Replace "threeCol"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          limitWindows 7 $
            ThreeCol 1 (3 / 100) (1 / 2)

threeRow =
  renamed [Replace "threeRow"] $
    smartBorders $
      addTabs shrinkText myTabTheme $
        subLayout [] (smartBorders Simplest) $
          limitWindows 7
          -- Mirror takes a layout and rotates it by 90 degrees.
          -- So we are applying Mirror to the ThreeCol layout.
          $
            Mirror $
              ThreeCol 1 (3 / 100) (1 / 2)

tabs =
  renamed [Replace "tabs"]
  -- I cannot add spacing to this layout because it will
  -- add spacing between window and tabs which looks bad.
  $
    tabbed shrinkText myTabTheme

tallAccordion =
  renamed
    [Replace "tallAccordion"]
    Accordion

wideAccordion =
  renamed [Replace "wideAccordion"] $
    Mirror Accordion

-- setting colors for tabs layout and tabs sublayout.
myTabTheme =
  def
    { fontName = myFont,
      activeColor = "#bd93f9",
      inactiveColor = "#44475a",
      activeBorderColor = "#bd93f9",
      inactiveBorderColor = "#44475a",
      activeTextColor = "#f8f8f2",
      inactiveTextColor = "#282c34"
    }

-- The layout hook
myLayoutHook =
  avoidStruts $
    mouseResize $
      windowArrange $
        toggleLayouts floats $
          mkToggle (NBFULL ?? NOBORDERS ?? EOT) myDefaultLayout
  where
    myDefaultLayout =
      withBorder myBorderWidth tall
        ||| magnify
        ||| noBorders monocle
        ||| floats
        ||| noBorders tabs
        ||| grid
        ||| threeCol
        ||| threeRow
        ||| tallAccordion
        ||| wideAccordion

------------------------------------------------------------------------
-- Window rules:

-- Execute arbitrary actions and WindowSet manipulations when managing
-- a new window. You can use this to, for example, always float a
-- particular program, or have a client always appear on a particular
-- workspace.
--
-- To find the property name associated with a program, use
-- > xprop | grep WM_CLASS
-- and click on the client you're interested in.
--
-- To match on the WM_NAME, you can use 'title' in the same way that
-- 'className' and 'resource' are used below.
--
myManageHook :: XMonad.Query (Data.Monoid.Endo WindowSet)
myManageHook =
  composeAll
    -- 'doFloat' forces a window to float.  Useful for dialog boxes and such.
    -- using 'doShift ( myWorkspaces !! 7)' sends program to workspace 8!
    -- I'm doing it this way because otherwise I would have to write out the full
    -- name of my workspaces and the names would be very long if using clickable workspaces.
    [ className =? "confirm" --> doFloat,
      className =? "file_progress" --> doFloat,
      className =? "dialog" --> doFloat,
      className =? "download" --> doFloat,
      className =? "error" --> doFloat,
      className =? "Gimp" --> doFloat,
      className =? "notification" --> doFloat,
      className =? "pinentry-gtk-2" --> doFloat,
      className =? "splash" --> doFloat,
      className =? "toolbar" --> doFloat,
      title =? "Oracle VM VirtualBox Manager" --> doFloat,
      title =? "Mozilla Firefox" --> doShift (myWorkspaces !! 1),
      className =? "brave-browser" --> doShift (myWorkspaces !! 1),
      className =? "qutebrowser" --> doShift (myWorkspaces !! 1),
      className =? "mpv" --> doShift (myWorkspaces !! 7),
      className =? "Gimp" --> doShift (myWorkspaces !! 8),
      className =? "VirtualBox Manager" --> doShift (myWorkspaces !! 4),
      (className =? "brave-browser" <&&> resource =? "Dialog") --> doFloat,
      isFullscreen --> doFullFloat
    ]
    <+> namedScratchpadManageHook myScratchPads

------------------------------------------------------------------------
-- Event handling

-- * EwmhDesktops users should change this to ewmhDesktopsEventHook

--
-- Defines a custom handler function for X Events. The function should
-- return (All True) if the default handler is to be run afterwards. To
-- combine event hooks use mappend or mconcat from Data.Monoid.
--

------------------------------------------------------------------------
-- Status bars and logging

-- Perform an arbitrary action on each internal state change or X event.
-- See the 'XMonad.Hooks.DynamicLog' extension for examples.
--
------------------------------------------------------------------------
-- Startup hook

-- Perform an arbitrary action each time xmonad starts or is restarted
-- with mod-q.  Used by, e.g., XMonad.Layout.PerWorkspace to initialize
-- per-workspace layout choices.
-- By default, do nothing.
myStartupHook :: X ()
myStartupHook = do
  -- spawnOnce "picom --experimental-backends &"
  -- spawnOnce "nm-applet &"
  -- spawnOnce "blueman-applet &"
  -- spawnOnce "transmission-gtk -m &"
  spawnOnce "feh --bg-fill ~/Pictures/wallpaper.png &"
  -- spawnOnce "dunst &"
  -- spawnOnce "ferdi &"
  -- spawnOnce "fusuma -d &"
  -- spawnOnce "fcitx5 &"
  -- spawnOnce "~/.config/scripts/wait.sh &"
  -- spawnOnce "/usr/bin/lxpolkit&"
  spawnOnce "sudo tzupdate&"
  setWMName "LG3D"

-- spawnOnce "rclone mount --allow-other --vfs-cache-mode full --vfs-cache-max-age 999h --vfs-read-chunk-size 8M --cache-writes --daemon x:/ ~/x &"

------------------------------------------------------------------------
-- Now run xmonad with all the defaults we set up.

-- Run xmonad with the settings you specify. No need to modify this.
--
main :: IO ()
main = do
  -- Launching three instances of xmobar on their monitors.
  xmproc0 <- spawnPipe "xmobar -x 0 -r $HOME/.config/xmobar/xmobarrc"
  -- xmproc1 <- spawnPipe "xmobar -x 1 $HOME/.config/xmobar/xmobarrc1"
  -- xmproc2 <- spawnPipe "xmobar -x 2 $HOME/.config/xmobar/xmobarrc2"
  -- the xmonad, ya know...what the WM is named after!
  xmonad $
    ewmh
      def
        { manageHook = myManageHook <+> manageDocks,
          handleEventHook = docksEventHook,
          -- Uncomment this line to enable fullscreen support on things like YouTube/Netflix.
          -- This works perfect on SINGLE monitor systems. On multi-monitor systems,
          -- it adds a border around the window if screen does not have focus. So, my solution
          -- is to use a keybinding to toggle fullscreen noborders instead.  (M-<Space>)
          -- <+> fullscreenEventHook
          modMask = myModMask,
          terminal = myTerminal,
          startupHook = myStartupHook,
          layoutHook = myLayoutHook,
          workspaces = myWorkspaces,
          borderWidth = myBorderWidth,
          normalBorderColor = myNormalBorderColor,
          focusedBorderColor = myFocusedBorderColor,
          logHook =
            dynamicLogWithPP $
              namedScratchpadFilterOutWorkspacePP $
                xmobarPP
                  { -- the following variables beginning with 'pp' are settings for xmobar.
                    ppOutput = hPutStrLn xmproc0, -- xmobar on monitor 1
                    -- >> hPutStrLn xmproc1 x -- xmobar on monitor 2
                    -- >> hPutStrLn xmproc2 x, -- xmobar on monitor 3
                    ppCurrent = xmobarColor "#98be65" "" . wrap "[" "]", -- Current workspace
                    ppVisible = xmobarColor "#98be65" "" . clickable, -- Visible but not current workspace
                    ppHidden = xmobarColor "#82AAFF" "" . wrap "*" "" . clickable, -- Hidden workspaces
                    ppHiddenNoWindows = xmobarColor "#c792ea" "" . clickable, -- Hidden workspaces (no windows)
                    ppTitle = xmobarColor "#b3afc2" "" . shorten 60, -- Title of active window
                    ppSep = "<fc=#666666> <fn=1>|</fn> </fc>", -- Separator character
                    ppUrgent = xmobarColor "#C45500" "" . wrap "!" "!", -- Urgent workspace
                    ppExtras = [windowCount], -- # of windows current workspace
                    ppOrder = \(ws : l : t : ex) -> [ws, l] ++ ex ++ [t] -- order of things in xmobar
                  }
        }
      `additionalKeysP` myKeys
