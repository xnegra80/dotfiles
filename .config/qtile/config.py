from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook

from typing import List

import os
import subprocess

mod = "mod4"

home = os.path.expanduser('~')


@hook.subscribe.startup_once
def autostart():
  subprocess.call([os.path.expanduser('~/.config/qtile/autostart.sh')])


keys = [
    
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),
    Key([mod], "space", lazy.layout.next()),
    Key([mod], "Delete",   lazy.spawn(
        [os.path.expanduser('~/.config/qtile/power.sh')])),
    Key(
        [mod], "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod], "l",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize(),
    ),
    Key(
        [mod], "m",
        lazy.layout.maximize(),
    ),
    Key(
        [mod, "shift"], "f",
        lazy.window.toggle_floating(),
    ),
    Key(
        [mod], "f",
        lazy.window.toggle_fullscreen(),
    ),
    Key(
        [mod], "Print",
        lazy.spawn(
            'maim -i "$(xdotool getactivewindow)" | xclip -sel clip -t image/png')
    ),
    Key(
        [mod], "Print",
        lazy.spawn('maim | xclip -sel clip -t image/png'),
    ),
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
    ),
    Key(
        [mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
    ),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.widget['pulsevolume'].increase_vol()),
    Key([], "XF86AudioLowerVolume", lazy.widget['pulsevolume'].decrease_vol()),
    Key([], "XF86AudioMute", lazy.widget['pulsevolume'].mute()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod, 'shift'], "d", lazy.spawn('rofi -show run')),
]

groups = [Group(i) for i in "1234567890"]

for i in groups:
  keys.extend([
      Key([mod], i.name, lazy.group[i.name].toscreen()),
      Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True)),
  ])

layout_theme = {"border_width": 2,
                "margin": 5,
                "border_focus": "bd93f9",
                "border_normal": "44475a"
                }

layouts = [
    # layout.Max(),
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(),
    layout.Tile(shift_windows=True, **layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font='Cantwell, Font Awesome 5 Free',
    fontsize=12,
    padding=0,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(),
                widget.WindowName(),
                widget.Systray(),
                widget.Spacer(length=10),
                widget.TextBox(text=""),
                widget.Backlight(backlight_name='intel_backlight'),
                widget.Spacer(length=10),
                widget.Battery(
                    format='{char} {percent:2.0%} {hour:d}:{min:02d}'),

                widget.PulseVolume(volume_app="pavucontrol", step=5),
                widget.ThermalSensor(),
                widget.Wlan(interface='wlp0s20f3',
                            format='{essid} {percent:2.0%}'),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
                widget.TextBox(text="⟳"),
                widget.Pacman(),
                widget.CurrentLayoutIcon(scale=.45),
            ],
            24,
            background='#282a36', opacity=.85
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
