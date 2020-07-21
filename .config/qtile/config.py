from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook


from typing import List

import os
import subprocess
import re

mod = "mod4"

group_names = " a"


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(os.path.expanduser('~/.config/qtile/autostart.sh'))


keys = [

    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # Grow windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),

    Key([mod], "space", lazy.layout.next()),
    Key([mod, 'control'], "v", lazy.group[group_names[9]].toscreen(
        toggle=False), lazy.spawn(
        [os.path.expanduser('~/.config/qtile/vm.sh')])),
    Key([mod, "control"], "d", lazy.spawn(
        [os.path.expanduser('~/.config/qtile/monitor_layout.sh')])),
    Key([mod, "control"], "p", lazy.spawn(
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
    # Key(
    #     [mod], "m",
    #     lazy.layout.maximize(),
    # ),
    Key(
        [mod, "shift"], "f",
        lazy.window.toggle_floating(),
    ),
    Key(
        [mod], "f",
        lazy.window.toggle_fullscreen(),
    ),
    # Monitors
    Key([mod], "period",
        lazy.next_screen(),
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        ),





    Key([mod], "Print", lazy.spawn('rofi-screenshot -s')),
    Key(
        [], "Print",
        lazy.spawn('rofi-screenshot')
    ),
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
    ),
    Key([mod], "space", lazy.layout.next()),

    # XF86 Buttons
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.widget['volume'].increase_vol()),
    Key([], "XF86AudioLowerVolume", lazy.widget['volume'].decrease_vol()),
    Key([], "XF86AudioMute", lazy.widget['volume'].mute()),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, 'shift'], "Tab", lazy.prev_layout()),
    Key([mod, "shift"], "q", lazy.window.kill()),
    Key([mod, "shift"], "r", lazy.restart()),

    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod, 'shift'], "d", lazy.spawn('rofi -show run')),


    Key([mod], "Return", lazy.spawn("alacritty")),

    Key([mod], "e", lazy.spawn('caja')),
    Key([mod, "shift"], "e", lazy.spawn('sudo caja')),
    Key([mod, "control"], "e", lazy.spawn('ranger')),
    Key([mod], "i", lazy.spawn('killall insync'), lazy.spawn('insync start')),
    Key([mod], "v", lazy.spawn('pavucontrol')),
    Key([mod, 'shift'], "t", lazy.spawn('sudo timeshift')),


    Key([mod], "m", lazy.group[group_names[1]].toscreen(
        toggle=False), lazy.spawn('mailspring')),

    Key([mod], "w", lazy.group[group_names[2]].toscreen(
        toggle=False), lazy.spawn('vivaldi-stable')),

    Key([mod], "c", lazy.group[group_names[4]].toscreen(
        toggle=False), lazy.spawn('code')),

    Key([mod], "s", lazy.group[group_names[5]].toscreen(
        toggle=False), lazy.spawn('alacritty -e spt')),

    Key([mod], "t", lazy.group[group_names[7]].toscreen(
        toggle=False), lazy.spawn('tableplus')),
    Key([mod], "p", lazy.group[group_names[7]].toscreen(
        toggle=False), lazy.spawn('postman')),

    Key([mod], "r", lazy.group[group_names[9]].toscreen(
        toggle=False), lazy.spawn('remmina')),
]


groups = [
    Group(group_names[1], layout='monadtall'),
    Group(group_names[2], layout='monadtall'),
    Group(group_names[3], layout='matrix'),
    Group(group_names[4], layout='max'),
    Group(group_names[5], layout='monadtall'),
    Group(group_names[6], layout='monadtall'),
    Group(group_names[7], layout='max'),
    Group(group_names[8], layout='max'),
    Group(group_names[9], layout='monadtall'),
]

for i, group in enumerate(groups, 1):
    keys.extend([
        Key([mod], str(i), lazy.group[group.name].toscreen()),
        Key([mod, "shift"], str(i),
            lazy.window.togroup(group.name, switch_group=True)),
    ])

layout_theme = {"border_width": 0,
                "margin": 2,
                "border_focus": "bd93f9",
                "border_normal": "44475a",
                "single_border_width": 0,
                "single_margin": 0
                }

layouts = [
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.Max(),
    # layout.RatioTile(),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font='Roboto, Font Awesome 5 Free, Font Awesome 5 Brands',
    fontsize=12,
    padding=0,
    foreground='f8f8f2'
)
extension_defaults = widget_defaults.copy()


def get_widgets():
    return [
        widget.GroupBox(urgent_alert_method='text',
                        highlight_method='text', this_current_screen_border='bd93f9'),
        widget.Spacer(length=10),
        widget.WindowName(),
        widget.Systray(),
        widget.Spacer(length=10),
        widget.CPUGraph(line_width=1, graph_color='50fa7b',
                        border_width=0, fill_color='50fa7b'),
        widget.MemoryGraph(line_width=1, graph_color='ff79c6',
                           border_width=0, fill_color='ff79c6'),
        widget.SwapGraph(line_width=1, graph_color='f1fa8c',
                         border_width=0, fill_color='f1fa8c'),
        widget.Spacer(length=10),
        widget.TextBox(text=" ", foreground='8be9fd'),
        widget.ThermalSensor(foreground='8be9fd'),
        widget.Spacer(length=5),

        widget.Spacer(length=5, background='44475a'),
        widget.Backlight(backlight_name='intel_backlight',
                         format='{percent: 2.0%}', foreground='ff79c6', background='44475a'),
        widget.Spacer(length=5, background='44475a'),

        widget.Spacer(length=5),
        widget.Battery(
            format='{char} {percent:2.0%}',
            unknown_char='',
            charge_char='',
            empty_char='',
            discharge_char='',
            foreground='50fa7b'
        ),
        widget.Spacer(length=5),

        widget.Spacer(length=5, background='44475a'),
        widget.TextBox(text=" ", foreground='f1fa8c',
                       background='44475a'),
        widget.Volume(step=5, foreground='f1fa8c',
                      background='44475a'),
        widget.Spacer(length=5, background='44475a'),

        widget.Spacer(length=5),
        widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
        widget.Spacer(length=5),

        widget.Spacer(length=5, background='44475a'),
        widget.TextBox(text="⟳ ", background='44475a'),
        widget.Pacman(execute='alacritty -e yay -Syu',
                              background='44475a'),
        widget.Spacer(length=5, background='44475a'),

        widget.Spacer(length=5),
        widget.CurrentLayoutIcon(scale=.45),
    ]


screens = [
    Screen(
        top=bar.Bar(get_widgets(),
                    24,
                    background='#282a36', opacity=.85
                    ),
    ),
    Screen(
        bottom=bar.Bar(get_widgets(),
                       24,
                       background='#282a36', opacity=.85
                       ),
    ),
    Screen(
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod, 'shift'], "Button1", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {"role": "EventDialog"},
    {"role": "Msgcompose"},
    {"role": "Preferences"},
    {"role": "pop-up"},
    {"role": "prefwindow"},
    {"role": "task_dialog"},
    {"wname": "Module"},
    {"wname": "anydesk"},
    {"wname": "galculator"},
    {"wname": "Insync"},
    {"wname": "Picture-in-picture"},
    {"wname": "Search Dialog"},
    {"wname": "Goto"},
    {"wname": "IDLE Preferences"},
    {"wname": "Sozi"},
    {"wname": "Create new database"},
    {"wname": "Preferences"},
    {"wname": "File Transfer"},
    {"wname": 'branchdialog'},
    {"wname": 'pinentry'},
    {"wname": 'confirm'},
    {"wmclass": 'dialog'},
    {"wmclass": 'blueman-manager'},
    {"wmclass": 'download'},
    {"wmclass": 'error'},
    {"wmclass": 'file_progress'},
    {"wmclass": 'notification'},
    {"wmclass": 'splash'},
    {"wmclass": 'toolbar'},
    {"wmclass": 'confirmreset'},
    {"wmclass": 'makebranch'},
    {"wmclass": 'maketag'},
    {"wmclass": 'Dukto'},
    {"wmclass": 'Tilda'},
    {"wmclass": "GoldenDict"},
    {"wmclass": "Synapse"},
    {"wmclass": "TelegramDesktop"},
    {"wmclass": "notify"},
    {"wmclass": "Lxappearance"},
    {"wmclass": "Oblogout"},
    {"wmclass": "Pavucontrol"},
    {"wmclass": "Skype"},
    {"wmclass": "Eog"},
    {"wmclass": "Rhythmbox"},
    {"wmclass": "obs"},
    {"wmclass": "Gufw.py"},
    {"wmclass": "Catfish"},
    {"wmclass": "LibreOffice 3.4"},
    {"wmclass": 'ssh-askpass'},
    {"wmclass": "Mlconfig"},
], **layout_theme)
auto_fullscreen = True
bring_front_click = False
focus_on_window_activation = "smart"
floating_types = ["notification", "toolbar", "splash", "dialog",
                  "utility", "menu", "dropdown_menu", "popup_menu", "tooltip,dock",
                  ]
wmname = "LG3D"
