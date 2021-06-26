import qualified Codec.Binary.UTF8.String as UTF8
import qualified DBus as D
import qualified DBus.Client as D
import XMonad
import XMonad.Hooks.DynamicLog
import XMonad.Hooks.EwmhDesktops
import XMonad.Hooks.ManageDocks (avoidStruts)
import XMonad.Hooks.ManageHelpers
import XMonad.Hooks.SetWMName
import XMonad.Hooks.StatusBar
import XMonad.Hooks.StatusBar.PP
import XMonad.Layout.Magnifier
import XMonad.Layout.ThreeColumns
import XMonad.Util.EZConfig
import XMonad.Util.Loggers
import XMonad.Util.SpawnOnce
import XMonad.Util.Ungrab

-- Colours
fg = "#ebdbb2"

bg = "#282828"

gray = "#a89984"

bg1 = "#3c3836"

bg2 = "#505050"

bg3 = "#665c54"

bg4 = "#7c6f64"

green = "#b8bb26"

darkgreen = "#98971a"

red = "#fb4934"

darkred = "#cc241d"

yellow = "#fabd2f"

blue = "#83a598"

purple = "#d3869b"

aqua = "#8ec07c"

white = "#eeeeee"

pur2 = "#5b51c9"

blue2 = "#2266d0"

main :: IO ()
main = do
  dbus <- D.connectSession
  D.requestName
    dbus
    (D.busName_ "org.xmonad.Log")
    [D.nameAllowReplacement, D.nameReplaceExisting, D.nameDoNotQueue]

  xmonad
    . ewmhFullscreen
    . ewmh
    -- . withEasySB (statusBarProp "" (pure def)) defToggleStrutsKey
    -- . withEasySB (statusBarProp "xmobar ~/.config/xmobar/xmobarrc" (pure myXmobarPP)) defToggleStrutsKey
    $ myConfig {logHook = dynamicLogWithPP (myLogHook dbus)} -- Use custom layouts

myConfig =
  def
    { modMask = mod4Mask, -- Rebind Mod to the Super key
      startupHook = myStartupHook, -- Start certain programs
      manageHook = myManageHook, -- Match on certain windows
      layoutHook = myLayout -- Use custom layouts
    }
    `additionalKeysP` [ ("M-S-z", spawn "xscreensaver-command -lock"),
                        ("M-S-=", unGrab *> spawn "scrot -s"),
                        ("M-]", spawn "firefox")
                      ]

myStartupHook :: X ()
myStartupHook = do
  spawnOnce "picom --experimental-backends &"
  spawnOnce "nm-applet &"
  spawnOnce "volumeicon &"
  spawnOnce "blueman-applet &"
  -- spawnOnce "trayer --edge top --align right --widthtype request --padding 6 --SetDockType true --SetPartialStrut true --expand true --monitor 0 --transparent true --alpha 0 --tint 0x282c34  --height 16 &"
  -- spawnOnce "trayer --edge top --align right --SetDockType true --SetPartialStrut true --expand true --transparent true --tint 0x5f5f5f --height 18 &"
  -- spawnOnce "trayer --edge top --align right --widthtype request --padding 6 --SetDockType true --SetPartialStrut true --expand true --monitor 1 --transparent true --alpha 0 --tint 0x282c34  --height 22 &"
  spawnOnce "dunst &"
  spawnOnce "fcitx5 &"
  spawnOnce "feh --bg-fill ~/Pictures/wallpaper.png &"
  spawnOnce "fusuma -d &"
  spawnOnce "/usr/bin/lxpolkit &"
  spawnOnce "sudo tzupdate &"
  setWMName "LG3D"
  spawnOnce "sudo tzupdate &"

myManageHook :: ManageHook
myManageHook =
  composeAll
    [ className =? "Gimp" --> doFloat,
      isDialog --> doFloat
    ]

myLayout = avoidStruts $ tiled ||| Mirror tiled ||| Full ||| threeCol
  where
    threeCol = magnifiercz' 1.3 $ ThreeColMid nmaster delta ratio
    tiled = Tall nmaster delta ratio
    nmaster = 1 -- Default number of windows in the master pane
    ratio = 1 / 2 -- Default proportion of screen occupied by master pane
    delta = 3 / 100 -- Percent of screen to increment by when resizing panes

myLogHook :: D.Client -> PP
myLogHook dbus =
  def
    { ppOutput = dbusOutput dbus,
      ppCurrent = wrap ("%{F" ++ blue2 ++ "} ") " %{F-}",
      ppVisible = wrap ("%{F" ++ blue ++ "} ") " %{F-}",
      ppUrgent = wrap ("%{F" ++ red ++ "} ") " %{F-}",
      ppHidden = wrap " " " ",
      ppWsSep = "",
      ppSep = " | ",
      ppTitle = myAddSpaces 25
    }

-- Emit a DBus signal on log updates
dbusOutput :: D.Client -> String -> IO ()
dbusOutput dbus str = do
  let signal =
        (D.signal objectPath interfaceName memberName)
          { D.signalBody = [D.toVariant $ UTF8.decodeString str]
          }
  D.emit dbus signal
  where
    objectPath = D.objectPath_ "/org/xmonad/Log"
    interfaceName = D.interfaceName_ "org.xmonad.Log"
    memberName = D.memberName_ "Update"

myAddSpaces :: Int -> String -> String
myAddSpaces len str = sstr ++ replicate (len - length sstr) ' '
  where
    sstr = shorten len str
