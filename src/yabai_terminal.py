import yabai_tools, alfred_search
import swap_select
import argparse
import os, json, requests

def focus_direction(args):
    yabai_tools.focus_direction(args.direction, follow_focus=not args.no_mouse_follow)

def focus_on(args):
    if args.window_id == None:
        return
    yabai_tools.focus_to(args.window_id, follow_focus=not args.no_mouse_follow)

def close_window(args):
    if args.window_id == None:
        return
    yabai_tools.close_window(args.window_id)

def swap_to(args):
    if args.window_id == None:
        return
    yabai_tools.swap_to(args.window_id, follow_focus=not args.no_mouse_follow)

def swap_select_direction(args):
    swap_select.swap_select(args.direction, follow_focus=not args.no_mouse_follow, key_mod=args.key_mod)

def focus_display_direction(args):
    yabai_tools.focus_display(args.direction, follow_focus=not args.no_mouse_follow)

def send_to_display_direction(args):
    yabai_tools.send_to_display(args.direction, follow_focus=not args.no_mouse_follow)

def change_layout(args):
    yabai_tools.change_layout(args.layout)

def window_options(args):
    if args.toggle in ['float', 'zoom-parent', 'zoom-fullscreen', 'native-fullscreen', 'border']:
        yabai_tools.window_toggle(args.toggle, window_id=args.window_id)
    elif args.toggle == "focus":
        focus_on(args)
    elif args.toggle == "close":
        close_window(args)
    elif args.toggle == "swap":
        swap_to(args)



# Create the parser
my_parser = argparse.ArgumentParser(prog="yabai_terminal.py", 
                                    description='A Python implementation of more advanced yabai mathods')

subparsers = my_parser.add_subparsers()

focus_direction_parser = subparsers.add_parser("focus", help="Focus in the given direction")
focus_direction_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
focus_direction_parser.add_argument("--no-mouse-follow", action="store_true")
focus_direction_parser.set_defaults(func=focus_direction)

focus_on_parser = subparsers.add_parser("focus-on", help="Focus on a given window")
focus_on_parser.add_argument("--no-mouse-follow", action="store_true")
focus_on_parser.add_argument("--window-id")
focus_on_parser.set_defaults(func=focus_on)

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

window_parser = subparsers.add_parser("window", help="Toggle choices for the given window")
window_parser.add_argument("toggle", choices=['float', 'zoom-parent', 'zoom-fullscreen', 'native-fullscreen', 'border', 'focus', 'close', 'swap'])
window_parser.add_argument("--window-id")
window_parser.add_argument("--no-mouse-follow", action="store_true")
window_parser.set_defaults(func=window_options)

change_layout_parser = subparsers.add_parser("search", help="The manager for the Alfred Search Workflow")
change_layout_parser.add_argument("search")
change_layout_parser.set_defaults(func=alfred_search.search)

window_options_parser = subparsers.add_parser("window-options", help="The manager for the Alfred Window Workflow")
window_options_parser.add_argument("--window-id")
window_options_parser.add_argument("--open-alfred", action="store_true")
window_options_parser.set_defaults(func=alfred_search.window_options_menu)

window_list_parser = subparsers.add_parser("window-list")
window_list_parser.add_argument("--window-id")
window_list_parser.add_argument("--open-alfred", action="store_true")
window_list_parser.set_defaults(func=alfred_search.window_list)

# Execute the parse_args() method
args = my_parser.parse_args()
if (hasattr(args, 'func')):
    args.func(args)