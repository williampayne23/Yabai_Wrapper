import yabai_tools
import swap_select
import argparse
import os, json, requests

items = []

def focus_direction(args):
    yabai_tools.focus_direction(args.direction, follow_focus=not args.no_mouse_follow)

def swap_select_direction(args):
    swap_select.swap_select(args.direction, follow_focus=not args.no_mouse_follow, key_mod=args.key_mod)

def focus_display_direction(args):
    yabai_tools.focus_display(args.direction, follow_focus=not args.no_mouse_follow)

def send_to_display_direction(args):
    yabai_tools.send_to_display(args.direction, follow_focus=not args.no_mouse_follow)

def change_layout(args):
    yabai_tools.change_layout(args.layout)

def window_options(args):
    yabai_tools.window_toggle(args.toggle)

def search(args):
    output = {
        "items" : items
    }
    print(json.dumps(output))

def item(title, subtitle, arg, uid=None, item_type=None, autocomplete=None, icon=""):
    if autocomplete == None:
        autocomplete=title
    
    if icon!="":
        path = "./icons/{title}.png".format(title=title)
        if not os.path.isdir('./icons'):
            path = "./icons"
            access_rights = 0o755
            os.mkdir(path, access_rights)
        if not os.path.isfile(path):
            response = requests.get(icon)
            file = open(path, "wb")
            file.write(response.content)
            file.close()
        icon = path
    
    items.append(
        {
            "uid": uid,
            "type": item_type,
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
            "autocomplete": autocomplete,
            "icon": {
                "path": icon
            }
        })

# Create the parser
my_parser = argparse.ArgumentParser(prog="yabai_terminal.py", 
                                    description='A Python implementation of more advanced yabai mathods')

subparsers = my_parser.add_subparsers()

focus_direction_parser = subparsers.add_parser("focus", help="Focus in the given direction")
focus_direction_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
focus_direction_parser.add_argument("--no-mouse-follow", action="store_true")
focus_direction_parser.set_defaults(func=focus_direction)


swap_select_parser = subparsers.add_parser("swap-select", help="Move swap selection in the given direction, or swap")
swap_select_parser.add_argument("direction", choices=['north', 'south', 'east', 'west', 'swap'])
swap_select_parser.add_argument("--no-mouse-follow", action="store_true")
swap_select_parser.add_argument("--key-mod", action="store_true")
swap_select_parser.set_defaults(func=swap_select_direction)

focus_display_parser = subparsers.add_parser("focus-display", help="Focus to the display in the given direction")
focus_display_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
focus_display_parser.add_argument("--no-mouse-follow", action="store_true")
focus_display_parser.set_defaults(func=focus_display_direction)

send_to_display_parser = subparsers.add_parser("send-to-display", help="Send to the display in the given direction")
send_to_display_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
send_to_display_parser.add_argument("--no-mouse-follow", action="store_true")
send_to_display_parser.set_defaults(func=send_to_display_direction)

change_layout_parser = subparsers.add_parser("change-layout", help="Change between bsp, stack, and float layouts")
change_layout_parser.add_argument("layout", choices=['bsp', 'stack', 'float'])
change_layout_parser.set_defaults(func=change_layout)
item("grid layout", "Switch to grid layout", "change-layout bsp", icon="https://github.com/williampayne23/Yabai_Wrapper/blob/master/icons/border-all-solid.png")
item("stack layout", "Switch to stack layout", "change-layout stack", icon="https://github.com/williampayne23/Yabai_Wrapper/blob/master/icons/layer-group-solid.png")
item("free layout", "Switch to free layout", "change-layout float", icon="https://github.com/williampayne23/Yabai_Wrapper/blob/master/icons/window-restore-regular.png")



change_layout_parser = subparsers.add_parser("window", help="Toggle choices for the given window")
change_layout_parser.add_argument("toggle", choices=['float', 'zoom-parent', 'zoom-fullscreen', 'native-fullscreen', 'bordered'])
change_layout_parser.set_defaults(func=window_options)

change_layout_parser = subparsers.add_parser("search", help="The manager for the Alfred Search widget")
change_layout_parser.add_argument("search")
change_layout_parser.set_defaults(func=search)

# Execute the parse_args() method
args = my_parser.parse_args()
if (hasattr(args, 'func')):
    args.func(args)

"""
TODO
+ Moving spaces
+ Window close

+ BTT Control Bar
+ Alfred menu 
"""
