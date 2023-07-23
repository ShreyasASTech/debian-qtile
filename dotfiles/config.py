###############################################################
######################## -> Imports <- ########################
###############################################################
import os
import subprocess
import psutil
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
from libqtile.lazy import lazy

##############################################################
##### -> Mod Key, Default Terminal & Default App Menu <- #####
##############################################################
mod         =  "mod4"
myTerminal  =  "xfce4-terminal --dynamic-title-mode=before --hide-toolbar --hide-menubar --hide-scrollbar"
app_menu    =  "j4-dmenu-desktop"
launch_htop =  "xfce4-terminal --dynamic-title-mode=before --hide-toolbar --hide-menubar --hide-scrollbar -e htop"
myBrowser   =  "any-browser"

##############################################################
############### -> Keybindings & KeyChords <- ################
##############################################################
keys = [
    #---------------------------------#
    #---------( Window Ctrls )--------#
    #---------------------------------#

    # To close focused window
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    
    # Change focus to another window
    Key([mod], "left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "up", lazy.layout.up(), desc="Move focus up"),
    
    # Move focused windows (tiled) around the workspace
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),

    # enter fullscreen mode for the focused container
    Key([mod], "f", lazy.window.toggle_fullscreen()),

    # Toggle tiling / floating mode
    Key([mod], "space", lazy.window.toggle_floating()),
    
    # Toggle between different layouts
    Key([mod], "t", lazy.next_layout(), desc="Toggle between layouts"),

    # resize focused window using keyboard
    Key([mod], "equal", lazy.layout.grow()),
    Key([mod], "minus", lazy.layout.shrink()),
    Key([mod], "kp_add", lazy.layout.grow()),
    Key([mod], "kp_subtract", lazy.layout.shrink()),

    #---------------------------------#
    #--( Volume Ctrl Using Keyboard )-#
    #---------------------------------#
    Key([], "KP_Add", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ +2%'), desc="Increase Volume"),
    Key([], "KP_Subtract", lazy.spawn('pactl set-sink-volume @DEFAULT_SINK@ -2%'), desc="Decrease Volume"),
    Key([], "KP_Enter", lazy.spawn('pactl set-sink-mute @DEFAULT_SINK@ toggle'), desc="Mute/Unmute Volume"),
    Key([], "KP_Insert", lazy.spawn('pactl set-source-mute @DEFAULT_SOURCE@ toggle'), desc="Mute/Unmute Mic"),

    #---------------------------------#
    #-------( System Controls )-------#
    #---------------------------------#

    # Start a terminal
    Key([mod], "Return", lazy.spawn(myTerminal), desc="Launch terminal"),

    # Launch my browser
    Key([mod], "b", lazy.spawn(myBrowser), desc="Launch Browser"),

    # Start program launcher
    Key([mod], "p", lazy.spawn(app_menu), desc="Open Dmenu or alternative"),

    # Take a screenshot by pressing Prt Scr Key
    Key([], "Print", lazy.spawn('/home/user-name/.config/screencapture/screenshooter.sh'), desc="Take a screnshot"),

    # A small logout script
    KeyChord([mod, "shift"], "q", [
        Key([], "l", lazy.shutdown(), desc="Shutdown Qtile"),
        Key([], "r", lazy.spawn('sudo reboot'), desc="Reboot Computer"),
        Key([], "s", lazy.spawn('sudo poweroff'), desc="Shutdown Computer")],
    mode=True,
    name="(R)eboot (S)hutdown (L)ogout"
    ),

    # Kill a process by specifying name
    Key([mod], "k", lazy.spawn('/home/user-name/.config/dkill.sh'), desc="Kill a process by specifying name"),

    #---------------------------------#
    #------( Reconfigure Qtile )------#
    #---------------------------------#
    KeyChord([mod], "q", [
        Key([], "c", lazy.reload_config()),
        Key([], "r", lazy.restart())],
    mode=True,
    name="reconfigure"
    ),
]

##############################################################
############## -> Define Groups (Workspaces) <- ##############
##############################################################
groups = [
    Group("1", label="Terminal"),
    Group("2", label="TextEdit", matches=[Match(wm_class=["Geany", "lite-xl"])]),
    Group("3", label="Browse", matches=[Match(wm_class=["librewolf-default", "Brave-browser"])]),
    Group("4", label="Notes", matches=[Match(wm_class=["Joplin"])]),
    Group("5", label="Media", matches=[Match(wm_class=["vlc", "Audacity"])]),
    Group("6", label="Misc", matches=[Match(wm_class=["KeePassXC"])]),
]

##############################################################
################## -> Workspace Controls <- ##################
##############################################################

for i in groups:
    keys.extend([
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name),
            ),
    ])

##############################################################
####################### -> Layouts <- ########################
##############################################################

# Default properties for all layouts
layout_theme = {"border_width": 1,
                "border_focus": "900000"
                }

# Layouts
layouts = [
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.MonadWide(**layout_theme),
]

# Floating layout
floating_layout = layout.Floating(

    # Floating layout properties
    **layout_theme,

    # Floating rules
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="Pavucontrol"),  # Pulse Audio Volume Control GUI
        Match(wm_class="Galculator"),  # My preferred calculator
        Match(wm_class="KeePassXC"),  # Password Manager
        Match(wm_class="Pcmanfm"),  # GUI File Manager
        Match(wm_class="GParted"),  # Disks & Partition Manager
        Match(wm_class="Nitrogen")  # Wallpaper picker
        ]
)

##############################################################
########## -> Widgets (Qtile Bar Customisation) <- ###########
##############################################################

# Default widget properties
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)

# Default extension properties
extension_defaults = widget_defaults.copy()

screens = [Screen(
    top=bar.Bar([
    
        # Widgets
        widget.CurrentLayoutIcon(scale=.85),
        widget.Spacer(length=2),
        widget.Sep(padding=5, linewidth=2),
        widget.GroupBox(highlight_method="block", disable_drag="True",block_highlight_text_color="FFFFFF"),
        widget.Sep(padding=7, linewidth=2),
        widget.Chord(background="EAC802", foreground="000000", padding=6, fontshadow="FFFFFF"),
        widget.WindowName(foreground="02FFBF"),
        widget.Sep(padding=7, linewidth=2),
        widget.CPU(foreground="DAF7A6", format="CPU: {load_percent}%", update_interval=2, mouse_callbacks={'Button1' : lazy.spawn(launch_htop)}),
        widget.Sep(padding=7, linewidth=2),
        widget.Memory(foreground="FFC300", format="MEM:{MemUsed: .0f}{mm}", update_interval=2, mouse_callbacks={'Button1' : lazy.spawn(launch_htop)}),
        widget.Sep(padding=7, linewidth=2),
        widget.Volume(fmt='VOL: {}', update_interval=0.1, mouse_callbacks={'Button1' : lazy.spawn('pavucontrol')}),
        widget.Sep(padding=7, linewidth=2),
        widget.Clock(foreground="FF5733", format="%^a  %-d/%-m  %-l:%M", update_interval=60),
        widget.Spacer(length=2),
        ],
        
    # Qtile bar properties
    20,opacity=0.84),
    ),
]

##############################################################
#################### -> Mouse Controls <- ####################
##############################################################

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
]

##############################################################
#################### -> Miscellaneous <- #####################
##############################################################

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

##############################################################
###################### -> Autostart <- #######################
##############################################################

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])
    subprocess.call([home + '/wall-set.sh'])
wmname = "LG3D"
