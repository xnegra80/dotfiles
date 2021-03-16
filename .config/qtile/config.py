from libqtile.config import Key, Screen, Group, Drag, Click, Match
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook, extension

import helpers
import custom_widget
import os
import subprocess
from screeninfo import get_monitors

mod = "mod4"
alt = "mod1"
term = "alacritty"

autostart = [
    "picom",
    "feh --bg-fill ~/Pictures/wallpaper",
    "dunst",
    "ferdi",
    "fusuma -d",
    "fcitx5",
    "~/.config/scripts/wait.sh",
    "/usr/bin/lxpolkit",
    "sudo tzupdate",
    "insync start",
    "redshift -l geoclue2" "echo 'enabled' > ~/.keyboard",
]


def get_color(key):
    colors = dict(
        primary="#bd93f9",
        foreground="#f8f8f2",
        background="#282a36",
        grey="#44475a",
        green="#50fa7b",
        cyan="#8be9fd",
        pink="#ff79c6",
        yellow="#f1fa8c",
        orange="#ffb86c",
    )
    return colors[key]


# @hook.subscribe.client_new
# def window_match(window):
#     matches = {
#         "ferdi": 1,
#         "brave-browser": 2,
#         "reddit": 2,
#         "io.github.celluloid_player.Celluloid": 5,
#         "TablePlus": 7,
#         "lutris": 8,
#         "deluge": 9,
#         "insomnia": 9,
#         "spotify": 0,
#         "discord": "discord",
#         "mailspring": "mailspring",
#         "virt-viewer": "win",
#         "org.remmina.Remmina": "win",
#     }

#     for wmclass, group in matches.items():
#         if window.match(Match(wm_class=wmclass)):
#             window.togroup(str(group), switch_group=True)
#             break


# @hook.subscribe.startup_once
# def autostart():
#     subprocess.Popen(os.path.expanduser("~/.config/qtile/autostart.sh"))


keys = [
    # -----------------------------------*----------------------------------- #
    # ---------------------------Launch Applications------------------------- #
    # -----------------------------------*----------------------------------- #
    # GUI applications
    Key([mod], "b", lazy.spawn("timeshift-launcher")),
    # Key([mod], 'e', lazy.spawn('caja')),
    Key([mod], "g", lazy.spawn("lutris")),
    Key([mod], "i", lazy.spawn("insomnia")),
    Key([mod], "t", lazy.spawn("tableplus")),
    Key([mod], "v", lazy.spawn("pavucontrol")),
    Key([mod], "c", lazy.spawn("emacs")),
    Key([mod], "w", lazy.spawn("brave")),
    Key(
        [mod],
        "s",
        # lazy.spawn("spotify"),
        lazy.spawn([os.path.expanduser("~/.config/scripts/spotify.sh")]),
    ),
    Key(
        [mod],
        "o",
        lazy.group["discord"].toscreen(toggle=False),
    ),
    Key(
        [mod],
        "m",
        lazy.group["mailspring"].toscreen(toggle=False),
        lazy.spawn("mailspring"),
    ),
    Key(
        [mod],
        "p",
        lazy.spawn("killall picom"),
        lazy.spawn("picom"),
    ),
    Key([mod], "y", lazy.spawn("celluloid --mpv-options=--fs")),
    # CLI applications
    Key([mod], "Return", lazy.spawn(term)),
    Key([mod], "r", lazy.spawn(f"{term} --class reddit -e tuir")),
    Key([mod], "e", lazy.spawn(f"{term} -e sh -c 'sleep 0.1 && ranger'")),
    # rofi menus
    Key([mod], "d", lazy.spawn("rofi -show drun")),
    Key([mod, "shift"], "d", lazy.spawn("rofi -show run")),
    Key(
        [mod, "control"],
        "v",
        lazy.run_extension(
            extension.CommandSet(
                commands={
                    " Connect to Windows LTSC": 'virsh start win-vm & virt-viewer -f --domain-name win-vm & notify-send " VM connected"',
                    " Disconnect from Windows LTSC": 'virsh managedsave win-vm & killall virt-viewer & killall libvirtd & notify-send " VM suspended"',
                },
                dmenu_prompt="Virtual Machines",
            )
        ),
    ),
    Key(
        [mod, "control"],
        "r",
        lazy.run_extension(
            extension.CommandSet(
                commands={
                    " Connect to FXPrimus VPS": 'remmina -c ~/.local/share/remmina/vps_rdp_fxprimus_3-217-236-145.remmina & notify-send "Remote connected"',
                    " Disconnect all remote connections": 'remmina -q & notify-send "Remote disconnected"',
                },
                dmenu_prompt="Remote Connections",
            )
        ),
    ),
    Key([mod, "control"], "n", lazy.spawn("networkmanager_dmenu")),
    Key(
        [mod, "control"],
        "c",
        lazy.spawn("rofi -show calc -modi calc -no-show-match -no-sort"),
    ),
    Key(
        [mod, "control"],
        "d",
        lazy.spawn([os.path.expanduser("~/.config/rofi/scripts/monitor-layout.sh")]),
    ),
    Key([mod, "control"], "b", lazy.spawn("rofi-bluetooth")),
    Key([], "Print", lazy.spawn("rofi-screenshot")),
    Key([mod], "Print", lazy.spawn("rofi-screenshot -s")),
    Key(
        [mod, "control"],
        "p",
        lazy.run_extension(
            extension.CommandSet(
                commands={
                    " Lock": "xset dpms force off",
                    " Shutdown": "systemctl poweroff",
                    " Reboot": "systemctl reboot",
                    " Logout": lazy.shutdown(),
                    " Hibernate": "systemctl hibernate",
                    " Suspend": "systemctl suspend",
                },
                dmenu_prompt="Power",
            )
        ),
    ),
    # -----------------------------------*----------------------------------- #
    # --------------------------Window Manipulation-------------------------- #
    # -----------------------------------*----------------------------------- #
    # Layout
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),
    Key([mod, "shift"], "q", lazy.window.kill()),
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
    # Window sizes
    Key([mod], "h", lazy.layout.grow(), lazy.layout.increase_nmaster()),
    Key([mod], "l", lazy.layout.shrink(), lazy.layout.decrease_nmaster()),
    Key([mod], "n", lazy.layout.normalize()),
    # Key([mod], 'm', lazy.layout.maximize()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    # Monitors
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),
    Key([mod, "shift"], "space", lazy.layout.rotate(), lazy.layout.flip()),
    Key([mod], "space", lazy.layout.next()),
    # -----------------------------------*----------------------------------- #
    # ------------------------------XF86 Buttons----------------------------- #
    # -----------------------------------*----------------------------------- #
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.widget["volume"].increase_vol()),
    Key([], "XF86AudioLowerVolume", lazy.widget["volume"].decrease_vol()),
    Key([], "XF86AudioMute", lazy.widget["volume"].mute()),
    Key([mod, "shift"], "r", lazy.restart()),
]

groups = [
    Group("1", label="", layout="stack", spawn=autostart),
    Group("2", label="", layout="monadtall"),
    Group("3", label="", layout="ratiotile"),
    Group("4", label="", layout="monadtall"),
    Group("5", label="", layout="monadtall"),
    Group("6", label="6", layout="monadtall"),
    Group("7", label="", layout="stack"),
    Group("8", label="", layout="stack"),
    Group("9", label="", layout="monadtall"),
    Group("0", label="", layout="monadtall"),
    Group(
        "mailspring",
        label="",
        layout="monadtall",
        spawn="mailspring",
        matches=[Match(wm_class="mailspring")],
    ),
    Group(
        "telegram",
        label="",
        layout="monadtall",
        spawn="telegram-desktop",
        matches=[Match(wm_class="telegram-desktop")],
    ),
    Group(
        "discord",
        label="",
        layout="monadtall",
        matches=[Match(wm_class="discord")],
    ),
    # Group("win", label="", layout="monadtall", persist=False),
]

for i in range(10):
    name = str(i)
    keys.extend(
        [
            Key([mod], name, lazy.group[name].toscreen()),
            Key([mod, "shift"], name, lazy.window.togroup(name, switch_group=True)),
        ]
    )

layout_theme = dict(
    border_width=2,
    margin=5,
    border_focus=get_color("primary"),
    border_normal=get_color("grey"),
)

layouts = [
    layout.Stack(**layout_theme, num_stacks=1),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Columns(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.RatioTile(**layout_theme),
    # layout.Max(),
    # layout.Tile(shift_windows=True, **layout_theme),
    # layout.TreeTab(
    #     **layout_theme,
    #     active_bg=get_color('primary'),
    #     active_fg=get_color('foreground'),
    #     bg_color=get_color('background'),
    #     inactive_bg=get_color('background'),
    #     inactive_fg=get_color('yellow'),
    #     section_fontsize=0,
    #     section_top=0,
    #     section_left=0,
    #     section_padding=0,
    #     padding_x=0,
    #     padding_y=0,
    #     padding_left=0,
    #     vspace=0,
    #     panel_width=50,
    #     previous_on_rm=True,
    # ),
    # layout.VerticalTile(),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="DejaVu Sans Mono, Font Awesome 5 Pro, Font Awesome 5 Brands",
    fontsize=11,
    padding=7,
    foreground=get_color("foreground"),
)

extension_defaults = widget_defaults.copy()


def get_graph_theme(key):
    return dict(
        line_width=1,
        graph_color=get_color(key),
        border_width=0,
        background=get_color("grey"),
        fill_color=get_color(key),
        width=45,
        samples=10,
    )


def toggle_keyboard(qtile):
    return qtile.cmd_spawn([os.path.expanduser("~/.config/qtile/keyboard.sh")])


def get_widgets():
    return [
        widget.CurrentLayoutIcon(background=get_color("grey"), scale=0.5),
        widget.GroupBox(
            urgent_alert_method="line",
            highlight_method="line",
            highlight_color=[get_color("background"), get_color("background")],
            this_current_screen_border=get_color("primary"),
            other_current_screen_border=get_color("cyan"),
            this_screen_border=get_color("yellow"),
            other_screen_border=get_color("cyan"),
            inactive=get_color("yellow"),
            disable_drag=True,
            borderwidth=2,
            spacing=0,
            padding=3,
        ),
        widget.TaskList(
            background=get_color("background"),
            foreground=get_color("foreground"),
            highlight_method="block",
            margin=0,
            icon_size=0,
            border=get_color("grey"),
            urgent_border=get_color("pink"),
        ),
        widget.Systray(padding=3),
        widget.CheckUpdates(
            custom_command="checkupdates && paru -Qua 2>/dev/null",
            colour_have_updates=get_color("pink"),
            display_format=" {updates:>2}",
            background=get_color("grey"),
        ),
        widget.GenPollText(
            func=custom_widget.get_crypto,
            foreground=get_color("yellow"),
            update_interval=60,
        ),
        widget.OpenWeather(
            location="london,uk",
            # location="hong kong",
            format="{location_city} {main_temp:.0f}°{units_temperature}",
            foreground=get_color("orange"),
            background=get_color("grey"),
        ),
        widget.GenPollText(
            func=custom_widget.get_bluetooth,
            foreground=get_color("cyan"),
            update_interval=1,
        ),
        custom_widget.Net(
            foreground=get_color("pink"),
            background=get_color("grey"),
            format="{down}↓↑{up}",
            interface=helpers.get_interface(),
        ),
        custom_widget.Wlan(
            foreground=get_color("green"),
            interface=helpers.get_interface(),
            format="{icon}{essid}{vpn}",
        ),
        widget.GenPollText(
            func=custom_widget.get_im,
            foreground=get_color("orange"),
            background=get_color("grey"),
            update_interval=1,
            mouse_callbacks={"Button1": toggle_keyboard},
        ),
        widget.GenPollText(
            func=custom_widget.get_ex,
            foreground=get_color("yellow"),
        ),
        widget.CPUGraph(**get_graph_theme("green")),
        widget.MemoryGraph(**get_graph_theme("cyan")),
        widget.SwapGraph(**get_graph_theme("primary")),
        custom_widget.ThermalSensor(foreground=get_color("cyan")),
        widget.Backlight(
            format=" {percent:2.0%}",
            foreground=get_color("pink"),
            background=get_color("grey"),
            backlight_name="intel_backlight",
        ),
        widget.Battery(
            format="{char} {percent:2.0%}",
            foreground=get_color("green"),
            unknown_char="",
            charge_char="",
            empty_char="",
            discharge_char="",
            full_char="",
            low_percentage=0.2,
            notify_below=0.2,
            update_interval=0.2,
        ),
        custom_widget.Volume(
            width=15,
            foreground=get_color("yellow"),
            background=get_color("grey"),
        ),
        widget.Volume(
            # width=65,
            foreground=get_color("yellow"),
            background=get_color("grey"),
            step=5,
        ),
        widget.Clock(foreground=get_color("orange"), format="%b %d %a %l:%M %p"),
    ]


screens = [
    Screen(
        top=bar.Bar(get_widgets(), 24, background=get_color("background"), opacity=0.9)
    )
    for _ in range(len(get_monitors()))
]


# @hook.subscribe.screen_change
def pop_monitor():
    while len(get_monitors()) < len(screens):
        screens.pop(-1)


# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        Match(wm_type="utility"),
        Match(wm_type="notification"),
        Match(wm_type="toolbar"),
        Match(wm_type="splash"),
        Match(wm_type="dialog"),
        Match(wm_class="file_progress"),
        Match(wm_class="confirm"),
        Match(wm_class="dialog"),
        Match(wm_class="download"),
        Match(wm_class="error"),
        Match(wm_class="notification"),
        Match(wm_class="splash"),
        Match(wm_class="toolbar"),
        Match(func=lambda c: c.has_fixed_size()),
    ],
    **layout_theme,
)
auto_fullscreen = False
bring_front_click = False
focus_on_window_activation = "smart"
floating_types = [
    "notification",
    "toolbar",
    "splash",
    "dialog",
    "utility",
    "menu",
    "dropdown_menu",
    "popup_menu",
    "tooltip,dock",
]
wmname = "LG3D"
