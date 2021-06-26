from libqtile.config import Key, Screen, Group, Drag, Click, Match, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, extension

import helpers
import custom_widget
import os
from screeninfo import get_monitors

mod = "mod4"
term = "alacritty"
tui = "alacritty -e env COLUMNS= LINES= "

autostart = [
    "picom --experimental-backends",
    "nm-applet",
    "blueman-applet",
    "transmission-gtk -m",
    "feh --bg-fill ~/Pictures/wallpaper.png",
    "dunst",
    "ferdi",
    "fusuma -d",
    "fcitx5",
    os.path.expanduser("~/.config/scripts/wait.sh"),
    "/usr/bin/lxpolkit",
    "sudo tzupdate",
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
    Key([mod], "c", lazy.spawn("emacsclient -c")),
    Key(
        [mod],
        "a",
        lazy.group["6"].toscreen(toggle=False),
        lazy.spawn("emacsclient -c -e '(org-agenda-list)'"),
    ),
    Key([mod], "w", lazy.spawn("brave --disable-features=SendMouseLeaveEvents")),
    # Key(
    #     [mod, "control"],
    #     "d",
    #     lazy.group["discord"].toscreen(toggle=False),
    #     lazy.spawn("discord"),
    # ),
    # Key(
    #     [mod],
    #     "m",
    #     lazy.group["mailspring"].toscreen(toggle=False),
    #     lazy.spawn("mailspring"),
    # ),
    Key(
        [mod],
        "p",
        lazy.spawn("killall picom"),
        lazy.spawn("picom --experimental-backends"),
    ),
    Key([mod], "y", lazy.spawn("celluloid --mpv-options=--fs")),
    # Scratchpads
    Key(
        [mod],
        "s",
        lazy.group["scratchpad"].dropdown_toggle("spotify"),
    ),
    Key(
        [mod],
        "m",
        lazy.group["scratchpad"].dropdown_toggle("bashtop"),
    ),
    Key([mod], "e", lazy.group["scratchpad"].dropdown_toggle("ranger")),
    # CLI applications
    Key([mod], "Return", lazy.spawn(term)),
    Key([mod], "r", lazy.spawn(f"{term} --class reddit -e tuir")),
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
                dmenu_ignorecase=True,
            )
        ),
    ),
    Key(
        [mod, "control"],
        "q",
        lazy.run_extension(
            extension.CommandSet(
                commands={
                    "alacritty": "coproc emacsclient -c ~/.config/alacritty/alacritty.yml > /dev/null",
                    "dunst": "coproc emacsclient -c ~/.config/dunst/dunstrc > /dev/null",
                    "fish": "coproc emacsclient -c ~/.config/fish/config.fish > /dev/null",
                    "fusuma": "coproc emacsclient -c ~/.config/fusuma/config.yml > /dev/null",
                    "picom": "coproc emacsclient -c ~/.config/picom/picom.conf > /dev/null",
                    "qtile": "coproc emacsclient -c ~/.config/qtile/config.py > /dev/null",
                },
                dmenu_prompt="Config Files",
                dmenu_ignorecase=True,
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
                dmenu_ignorecase=True,
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
        "s",
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
                dmenu_ignorecase=True,
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
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
]

groups = [
    Group("1", label="", layout="stack", spawn=autostart),
    Group("2", label="", layout="monadtall"),
    Group("3", label="", layout="ratiotile"),
    Group("4", label="", layout="monadtall"),
    Group("5", label="", layout="monadtall"),
    Group("6", label="", layout="monadtall"),
    Group("7", label="", layout="stack"),
    Group("8", label="", layout="stack"),
    Group(
        "9",
        label="",
        layout="monadtall",
        spawn="mailspring",
        matches=[Match(wm_class="mailspring")],
    ),
    Group(
        "0",
        label="",
        layout="monadtall",
        spawn=["telegram-desktop", "signal-desktop-beta"],
        matches=[Match(wm_class="telegram-desktop"), Match(wm_class="signal beta")],
    ),
    Group(
        "minus",
        label="",
        layout="monadtall",
        spawn="discord",
        matches=[Match(wm_class="discord")],
    ),
    Group(
        "equal", label="", layout="monadtall", matches=[Match(wm_class="virt-viewer")]
    ),
    ScratchPad(
        "scratchpad",
        [
            DropDown(
                "ranger",
                tui + "ranger",
                opacity=0.88,
                height=0.5,
                width=0.5,
                x=0.25,
                y=0.25,
            ),
            DropDown(
                "spotify",
                "spotify  --force-device-scale-factor=1",
                opacity=0.88,
                height=0.7,
                width=0.7,
                x=0.15,
                y=0.15,
            ),
            DropDown(
                "bashtop",
                tui + "bashtop",
                opacity=0.88,
                height=0.6,
                width=0.6,
                x=0.2,
                y=0.2,
            ),
        ],
    ),
]


for group in groups[:-1]:
    name = group.name
    keys.extend(
        [
            Key([mod], name, lazy.group[name].toscreen()),
            Key([mod, "shift"], name, lazy.window.togroup(name, switch_group=True)),
        ]
    )

layout_theme = dict(
    border_width=3,
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
    fontsize=12,
    padding=10,
    foreground=get_color("foreground"),
)

extension_defaults = widget_defaults.copy()


def get_widgets():
    return [
        widget.CurrentLayoutIcon(background=get_color("grey"), scale=0.35, padding=5),
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
            borderwidth=3,
            spacing=0,
            padding_x=10,
        ),
        widget.WindowName(fontsize=0),
        widget.CheckUpdates(
            custom_command="checkupdates && paru -Qua 2>/dev/null",
            colour_have_updates=get_color("primary"),
            display_format=" {updates:>2}",
            # background=get_color("grey"),
        ),
        # widget.Mpris2(
        #     objname="org.mpris.MediaPlayer2.spotify",
        #     display_metadata=["xesam:title", "xesam:artist"],
        #     foreground=get_color("pink"),
        # ),
        widget.OpenWeather(
            # location="london,uk",
            location="durham,uk",
            # location="hong kong",
            format="{location_city} {main_temp:.0f}°{units_temperature}",
            foreground=get_color("green"),
            # background=get_color("grey"),
        ),
        # custom_widget.Wlan(
        #     foreground=get_color("green"),
        #     interface=helpers.get_interface(),
        #     format="{icon}{essid}{vpn}",
        # ),
        # widget.GenPollText(
        #     func=custom_widget.get_im,
        #     foreground=get_color("orange"),
        #     background=get_color("grey"),
        #     update_interval=1,
        #     mouse_callbacks={"Button1": toggle_keyboard},
        # ),
        widget.GenPollText(
            func=custom_widget.get_ex,
            foreground=get_color("yellow"),
        ),
        custom_widget.Net(
            foreground=get_color("orange"),
            format="{down}↓↑{up}",
            interface=helpers.get_interface(),
            padding=5,
        ),
        custom_widget.ThermalSensor(foreground=get_color("cyan")),
        widget.Memory(format=" {MemPercent:2.0f}%", foreground=get_color("primary")),
        widget.NvidiaSensors(format=" {temp}°C", foreground=get_color("green")),
        widget.Backlight(
            format=" {percent:2.0%}",
            foreground=get_color("pink"),
            # background=get_color("grey"),
            backlight_name="intel_backlight",
        ),
        # custom_widget.Volume(
        #     width=25,
        #     foreground=get_color("yellow"),
        #     # background=get_color("grey"),
        # ),
        #
        widget.TextBox(text=" ", foreground=get_color("yellow"), padding=3),
        widget.Volume(
            # width=65,
            padding=0,
            foreground=get_color("yellow"),
            # background=get_color("grey"),
            step=5,
        ),
        widget.Spacer(
            length=10,
            # background=get_color("grey"),
        ),
        widget.Battery(
            format="{char} {percent:2.0%}",
            foreground=get_color("green"),
            unknown_char="",
            charge_char="",
            empty_char="",
            discharge_char="",
            full_char="",
            low_percentage=0.2,
            notify_below=0.2,
            update_interval=0.2,
        ),
        widget.Clock(foreground=get_color("orange"), format="%d %b %a %l:%M%p"),
        widget.Systray(padding=15),
        widget.Spacer(length=10),
    ]


screens = [
    Screen(
        top=bar.Bar(get_widgets(), 32, background=get_color("background"), opacity=0.9)
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
auto_fullscreen = True
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
