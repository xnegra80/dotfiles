from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook, extension

import helpers
import custom_widget
import os
import subprocess
from screeninfo import get_monitors

mod = 'mod4'


def get_color(key):
    colors = dict(
        primary='#bd93f9',
        foreground='#f8f8f2',
        background='#282a36',
        grey='#44475a',
        green='#50fa7b',
        cyan='#8be9fd',
        pink='#ff79c6',
        yellow='#f1fa8c',
        orange='#ffb86c'
    )
    return colors[key]


@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(os.path.expanduser('~/.config/qtile/autostart.sh'))


term = 'alacritty'

keys = [

    # rofi menus
    Key([mod], 'd', lazy.spawn('rofi -show drun')),
    Key([mod, 'shift'], 'd', lazy.spawn('rofi -show run')),
    Key([mod, 'control'], 'v', lazy.group['0'].toscreen(toggle=False),
        lazy.run_extension(
            extension.CommandSet(commands={
                ' Connect to Windows LTSC':
                'virsh start win-vm & virt-viewer -f --domain-name win-vm & notify-send " VM connected"',
                ' Disconnect from Windows LTSC':
                'virsh managedsave win-vm & killall virt-viewer & killall libvirtd & notify-send " VM suspended"'
            },
                dmenu_prompt='Virtual Machines'))),
    Key([mod, 'control'], 'r', lazy.group['0'].toscreen(toggle=False),
        lazy.run_extension(
            extension.CommandSet(commands={
                ' Connect to FXPrimus VPS':
                'remmina -c ~/.local/share/remmina/vps_rdp_fxprimus_3-217-236-145.remmina & notify-send " VM connected"',
                ' Disconnect all remote connections':
                'remmina -q & notify-send "Remote disconnected"'
            },
                dmenu_prompt='Remote Connections'))),
    Key([mod, 'control'], 'n', lazy.spawn('networkmanager_dmenu')),
    Key([mod, 'control'], 'c', lazy.spawn('rofi -show calc')),
    Key([mod, 'control'], 'd',
        lazy.spawn(
            [os.path.expanduser('~/.config/rofi/scripts/monitor-layout.sh')])),
    Key([mod, 'control'], 'b', lazy.spawn('rofi-bluetooth')),
    Key([], 'Print', lazy.spawn('rofi-screenshot')),
    Key([mod], 'Print', lazy.spawn('rofi-screenshot -s')),
    Key([mod, 'control'], 'p',
        lazy.run_extension(
            extension.CommandSet(commands={
                ' Lock': 'xset dpms force suspend; slock',
                ' Shutdown': 'systemctl poweroff',
                ' Reboot': 'killall lightdm',
                ' Logout': 'systemctl restart lightdm.service',
                ' Hibernate': 'systemctl hibernate',
                ' Suspend': 'systemctl suspend',
            },
                dmenu_prompt='Power'))),

    # -----------------------------------*----------------------------------- #
    # --------------------------Window Manipulation-------------------------- #
    # -----------------------------------*----------------------------------- #

    # Layout
    Key([mod], 'Tab', lazy.next_layout()),
    Key([mod, 'shift'], 'Tab', lazy.prev_layout()),

    Key([mod, 'shift'], 'q', lazy.window.kill()),

    # Switch between windows in current stack pane
    Key([mod], 'k', lazy.layout.up()),
    Key([mod], 'j', lazy.layout.down()),
    Key([mod], 'h', lazy.layout.left()),
    Key([mod], 'l', lazy.layout.right()),

    # Move windows up or down in current stack
    Key([mod, 'shift'], 'k', lazy.layout.shuffle_up()),
    Key([mod, 'shift'], 'j', lazy.layout.shuffle_down()),
    Key([mod, 'shift'], 'h', lazy.layout.shuffle_left()),
    Key([mod, 'shift'], 'l', lazy.layout.shuffle_right()),

    # Grow windows up or down in current stack
    Key([mod, 'control'], 'k', lazy.layout.grow_up()),
    Key([mod, 'control'], 'j', lazy.layout.grow_down()),
    Key([mod, 'control'], 'h', lazy.layout.grow_left()),
    Key([mod, 'control'], 'l', lazy.layout.grow_right()),
    Key([mod], 'space', lazy.layout.next()),

    # Window sizes
    Key(
        [mod],
        'h',
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
    ),
    Key(
        [mod],
        'l',
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
    ),
    Key(
        [mod],
        'n',
        lazy.layout.normalize(),
    ),
    Key(
        [mod], 'm',
        lazy.layout.maximize(),
    ),
    Key(
        [mod, 'shift'],
        'f',
        lazy.window.toggle_floating(),
    ),
    Key(
        [mod],
        'f',
        lazy.window.toggle_fullscreen(),
    ),
    # Monitors
    Key(
        [mod],
        'period',
        lazy.next_screen(),
    ),
    Key(
        [mod],
        'comma',
        lazy.prev_screen(),
    ),
    Key(
        [mod, 'shift'],
        'space',
        lazy.layout.rotate(),
        lazy.layout.flip(),
    ),
    Key([mod], 'space', lazy.layout.next()),

    # -----------------------------------*----------------------------------- #
    # ------------------------------XF86 Buttons----------------------------- #
    # -----------------------------------*----------------------------------- #

    Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl set +5%')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl set 5%-')),
    Key([], 'XF86AudioRaiseVolume', lazy.widget['volume'].increase_vol()),
    Key([], 'XF86AudioLowerVolume', lazy.widget['volume'].decrease_vol()),
    Key([], 'XF86AudioMute', lazy.widget['volume'].mute()),

    Key([mod, 'shift'], 'r', lazy.restart()),

    # -----------------------------------*----------------------------------- #
    # ---------------------------Launch Applications------------------------- #
    # -----------------------------------*----------------------------------- #

    # GUI applications
    Key([mod], 'b', lazy.spawn('timeshift-launcher')),
    Key([mod], 'e', lazy.spawn('caja')),
    Key([mod], 'm', lazy.spawn('geary')),
    Key([mod], 'p', lazy.spawn('postman')),
    Key([mod], 't', lazy.spawn('tableplus')),
    Key([mod], 'v', lazy.spawn('pavucontrol')),
    Key([mod], 'w', lazy.spawn('vivaldi-stable')),

    # CLI applications
    Key([mod], 'Return', lazy.spawn(term)),
    Key([mod], 'l', lazy.spawn(f'{term} -e ranger')),
    Key([mod], 'c', lazy.spawn(f'{term} --class nvim -e nvr')),  # fix resize
    Key([mod], 's', lazy.spawn(f'{term} --class spotify -e spt')),
]


@hook.subscribe.client_new
def window_match(window):
    matches = {
        'vivaldi-stable': 2,
        'nvim': 4,
        'spotify': 5,
        'geary': 6,
        'TablePlus': 7
    }

    if (window.name == 'Football Manager 2020'):
        window.fullscreen = False

    for wmclass, group in matches.items():
        if window.match(wmclass=wmclass):
            window.togroup(str(group), switch_group=True)
            break


groups = [
    Group('1', label='', layout='monadtall'),
    Group('2', label='', layout='monadtall'),
    Group('3', label='', layout='ratiotile'),
    Group('4', label='', layout='max'),
    Group('5', label='', layout='monadtall'),
    Group('6', label='', layout='monadtall'),
    Group('7', label='', layout='max'),
    Group('8', label='', layout='max'),
    Group('9', label='', layout='monadtall'),
    Group('0', label='', layout='monadtall'),
]

for i in range(10):
    name = str(i)
    keys.extend([
        Key([mod], name, lazy.group[name].toscreen()),
        Key([mod, 'shift'], name,
            lazy.window.togroup(name, switch_group=True)),
    ])

layout_theme = dict(border_width=0,
                    margin=2,
                    single_border_width=0,
                    single_margin=0)

layouts = [
    # layout.Stack(num_stacks=2),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Max(),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font='DejaVu Sans Mono, Font Awesome 5 Pro, Font Awesome 5 Brands',
    fontsize=11,
    padding=5,
    foreground=get_color('foreground'))

extension_defaults = widget_defaults.copy()


def get_graph_theme(key):
    return dict(line_width=1,
                graph_color=get_color(key),
                border_width=0,
                background=get_color('grey'),
                fill_color=get_color(key),
                width=65,
                samples=30)


def get_widgets():
    return [
        widget.GroupBox(
            urgent_alert_method='line',
            highlight_method='line',
            highlight_color=[get_color('background'),
                             get_color('background')],
            this_current_screen_border=get_color('primary'),
            other_current_screen_border=get_color('cyan'),
            this_screen_border=get_color('yellow'),
            other_screen_border=get_color('cyan'),
            inactive=get_color('yellow'),
            disable_drag=True,
            borderwidth=2,
            spacing=0,
            padding=3,
        ),
        widget.WindowName(),
        # widget.Systray(padding=3),
        widget.CheckUpdates(
            custom_command='checkupdates && pikaur -Qua 2>/dev/null',
            colour_have_updates=get_color('pink'),
            background=get_color('grey'),
            display_format='  {updates:>2} '),

        widget.GenPollText(func=custom_widget.get_bluetooth,
                           foreground=get_color('cyan'),
                           update_interval=1),
        custom_widget.Net(foreground=get_color('pink'),
                          background=get_color('grey'),
                          format='{down} ↓↑ {up}',
                          interface=helpers.get_interface()),
        custom_widget.Wlan(foreground=get_color('green'),
                           interface=helpers.get_interface(),
                           format=' {icon} {essid} '),

        widget.GenPollText(func=custom_widget.get_im,
                           foreground=get_color('orange'),
                           background=get_color('grey'),
                           update_interval=.2),
        widget.GenPollText(func=custom_widget.get_bitcoin,
                           foreground=get_color('yellow'),
                           update_interval=1),
        widget.CPUGraph(**get_graph_theme('green')),
        widget.MemoryGraph(**get_graph_theme('cyan')),
        widget.SwapGraph(**get_graph_theme('primary')),
        custom_widget.ThermalSensor(foreground=get_color('cyan'),
                                    threshold=60),
        widget.Backlight(format='  {percent:2.0%} ',
                         foreground=get_color('pink'),
                         background=get_color('grey'),
                         backlight_name='intel_backlight'),
        widget.Battery(format=' {char} {percent:2.0%} ',
                       foreground=get_color('green'),
                       unknown_char='',
                       charge_char='',
                       empty_char='',
                       discharge_char='',
                       full_char='',
                       low_percentage=.2,
                       notify_below=.2,
                       update_interval=.2),
        custom_widget.Volume(
            width=65, foreground=get_color('yellow'),
            background=get_color('grey'),
            step=5),
        widget.Clock(foreground=get_color('orange'),
                     format=' %b %d %a %I:%M %P '),

    ]


screens = [
    Screen(top=bar.Bar(
        get_widgets(), 24, background=get_color('background'), opacity=.9))
    for _ in range(2)


]

# Drag floating layouts.
mouse = [
    Drag([mod],
         'Button1',
         lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod],
         'Button3',
         lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], 'Button2', lazy.window.bring_to_front())
]

main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {
        'role': 'EventDialog'
    },
    {
        'role': 'Msgcompose'
    },
    {
        'role': 'Preferences'
    },
    {
        'role': 'pop-up'
    },
    {
        'role': 'prefwindow'
    },
    {
        'role': 'task_dialog'
    },
    {
        'wname': 'Module'
    },
    {
        'wname': 'anydesk'
    },
    {
        'wname': 'galculator'
    },
    {
        'wname': 'Insync'
    },
    {
        'wname': 'Picture-in-picture'
    },
    {
        'wname': 'Search Dialog'
    },
    {
        'wname': 'Goto'
    },
    {
        'wname': 'IDLE Preferences'
    },
    {
        'wname': 'Sozi'
    },
    {
        'wname': 'Create new database'
    },
    {
        'wname': 'Preferences'
    },
    {
        'wname': 'File Transfer'
    },
    {
        'wname': 'branchdialog'
    },
    {
        'wname': 'pinentry'
    },
    {
        'wname': 'confirm'
    },
    {
        'wmclass': 'dialog'
    },
    {
        'wmclass': 'blueman-manager'
    },
    {
        'wmclass': 'nm-connection-editor'
    },
    {
        'wmclass': 'download'
    },
    {
        'wmclass': 'error'
    },
    {
        'wmclass': 'file_progress'
    },
    {
        'wmclass': 'notification'
    },
    {
        'wmclass': 'splash'
    },
    {
        'wmclass': 'toolbar'
    },
    {
        'wmclass': 'confirmreset'
    },
    {
        'wmclass': 'makebranch'
    },
    {
        'wmclass': 'maketag'
    },
    {
        'wmclass': 'Dukto'
    },
    {
        'wmclass': 'Tilda'
    },
    {
        'wmclass': 'GoldenDict'
    },
    {
        'wmclass': 'Synapse'
    },
    {
        'wmclass': 'TelegramDesktop'
    },
    {
        'wmclass': 'notify'
    },
    {
        'wmclass': 'Lxappearance'
    },
    {
        'wmclass': 'Oblogout'
    },
    {
        'wmclass': 'Pavucontrol'
    },
    {
        'wmclass': 'Skype'
    },
    {
        'wmclass': 'Eog'
    },
    {
        'wmclass': 'Rhythmbox'
    },
    {
        'wmclass': 'obs'
    },
    {
        'wmclass': 'Gufw.py'
    },
    {
        'wmclass': 'Catfish'
    },
    {
        'wmclass': 'LibreOffice 3.4'
    },
    {
        'wmclass': 'ssh-askpass'
    },
    {
        'wmclass': 'Mlconfig'
    },
],
    **layout_theme)
auto_fullscreen = True
bring_front_click = False
focus_on_window_activation = 'smart'
floating_types = [
    'notification',
    'toolbar',
    'splash',
    'dialog',
    'utility',
    'menu',
    'dropdown_menu',
    'popup_menu',
    'tooltip,dock',
]
wmname = 'LG3D'
