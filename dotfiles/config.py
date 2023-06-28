import os
import subprocess
import psutil
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy

mod = "mod4"
myTerminal = "xfce4-terminal --dynamic-title-mode=before --hide-toolbar --hide-menubar --hide-scrollbar"
app_menu = "j4-dmenu-desktop"
launch_htop = "xfce4-terminal --dynamic-title-mode=before --hide-toolbar --hide-menubar --hide-scrollbar -e htop"
keys = [
Key([mod], "p", lazy.spawn(app_menu), desc="Open Dmenu or alternative"),
Key([mod], "space", lazy.window.toggle_floating()),
Key([mod], "f", lazy.window.toggle_fullscreen()),
Key([], "Print", lazy.spawn('/home/user-name/.config/screencapture/screenshooter.sh'), desc="Take a screnshot"),
KeyChord([mod, "shift"], "q", [
            Key([], "l", lazy.shutdown(), desc="Shutdown Qtile"),
            Key([], "r", lazy.spawn('sudo reboot'), desc="Reboot Computer"),
            Key([], "s", lazy.spawn('sudo poweroff'), desc="Shutdown Computer")],
            mode=True,
            name="(R)eboot (S)hutdown (L)ogout"
        ),



    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    # Key(
    #    [mod, "shift"],
    #    "Return",
    #    lazy.layout.toggle_split(),
    #    desc="Toggle between split and unsplit sides of stack",
    #),
    Key([mod], "Return", lazy.spawn(myTerminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "t", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    KeyChord([mod], "q", [
            Key([], "c", lazy.reload_config()),
            Key([], "r", lazy.restart())],
            mode=True,
            name="reconfigure"
            ),

    KeyChord([mod], "r", [
            Key([], "equal", lazy.layout.grow()),
            Key([], "minus", lazy.layout.shrink())],
            mode=True,
            name="resize"
            ),
    
    Key([], "KP_Add", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +2%'), desc="Increase Volume"),
    Key([], "KP_Subtract", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -2%'), desc="Decrease Volume"),
    Key([], "KP_Enter", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle'), desc="Mute/Unmute Volume"),
    Key([], "KP_Insert", lazy.spawn('pactl set-source-mute @DEFAULT_SOURCE@ toggle'), desc="Mute/Unmute Mic"),
]

groups = [
    Group("1", label="Terminal"),
    Group("2", label="TextEdit", matches=[Match(wm_class=["Geany", "lite-xl"])]),
    Group("3", label="Browse", matches=[Match(wm_class=["librewolf-default", "Brave-browser"])]),
    Group("4", label="Notes", matches=[Match(wm_class=["Joplin"])]),
    Group("5", label="Media", matches=[Match(wm_class=["vlc", "Audacity"])]),
    Group("6", label="Misc", matches=[Match(wm_class=["KeePassXC"])]),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {"border_width": 1,
                "border_focus": "900000"
                }

layouts = [
    # layout.Columns(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(**layout_theme),
    # layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=.85),
                widget.Spacer(length=2),
                widget.Sep(
                        padding=5,
                        linewidth=2
                        ),
                widget.GroupBox(
                        highlight_method="block",
                        disable_drag="True",
                        block_highlight_text_color="FFFFFF",
                        ),
                widget.Sep(
                        padding=7,
                        linewidth=2
                        ),
                widget.Chord(background="EAC802", foreground="000000", padding=6, fontshadow="FFFFFF"),
                widget.WindowName(foreground="02FFBF"),
                widget.Sep(
                        padding=7,
                        linewidth=2
                        ),
                widget.CPU(
                        foreground="DAF7A6",
                        format="CPU: {load_percent}%",
                        update_interval=2,
                        mouse_callbacks={'Button1' : lazy.spawn(launch_htop)}
                        ),
                widget.Sep(
                        padding=7,
                        linewidth=2
                        ),
                widget.Memory(
                        foreground="FFC300",
                        format="MEM:{MemUsed: .0f}{mm}",
                        update_interval=2,
                        mouse_callbacks={'Button1' : lazy.spawn(launch_htop)}
                        ),
                widget.Sep(
                        padding=7,
                        linewidth=2
                        ),
                # widget.Systray(),
                widget.Volume(
                        fmt='VOL: {}',
                        update_interval=0.1,
                        mouse_callbacks={'Button1' : lazy.spawn('pavucontrol')}
                        ),
                widget.Sep(
                        padding=7,
                        linewidth=2
                        ),
                widget.Clock(
                        foreground="FF5733",
                        format="%^a  %-d/%-m  %-l:%M",
                        update_interval=60
                        ),
                widget.Spacer(length=2),
                # widget.Sep(size_percent=70, padding=5, linewidth=2),
                # widget.QuickExit(default_text="[shutdown]",fontsize=14,foreground="c70032"),
            ],
            20,
            opacity=0.84,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(

    # Border properties
    **layout_theme,
    
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="Pavucontrol"),  # Pulse Audio Volume Control GUI
        ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# Autostart programs & services
@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
    subprocess.call([home + '/wall-set.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
