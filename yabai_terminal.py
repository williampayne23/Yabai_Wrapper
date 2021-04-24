import yabai_tools
import swap_select
import argparse
import os

def focus_direction(args):
    yabai_tools.focus_direction(args.direction, follow_focus=not args.no_focus)

def swap_select_direction(args):
    swap_select.swap_select(args.direction, follow_focus=not args.no_focus)
    if(args.key_mod):
        os.system('osascript ~/bin/Config/Tiling/yabaiEndSwitch.scpt')

def focus_display_direction(args):
    yabai_tools.focus_display(args.direction, follow_focus=not args.no_focus)

def send_to_display_direction(args):
    yabai_tools.send_to_display(args.direction, follow_focus=not args.no_focus)

def change_layout(args):
    yabai_tools.change_layout(args.layout)

def window_options(args):
    yabai_tools.window_toggle(args.toggle)

# Create the parser
my_parser = argparse.ArgumentParser(prog="yabai_terminal.py", 
                                    description='A Python implementation of more advanced yabai mathods')

subparsers = my_parser.add_subparsers()

focus_direction_parser = subparsers.add_parser("focus")
focus_direction_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
focus_direction_parser.add_argument("--no-focus", action="store_true")
focus_direction_parser.set_defaults(func=focus_direction)

swap_select_parser = subparsers.add_parser("swap-select")
swap_select_parser.add_argument("direction", choices=['north', 'south', 'east', 'west', 'swap'])
swap_select_parser.add_argument("--no-focus", action="store_true")
swap_select_parser.add_argument("--key-mod", action="store_true")
swap_select_parser.set_defaults(func=swap_select_direction)

focus_display_parser = subparsers.add_parser("focus-display")
focus_display_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
focus_display_parser.add_argument("--no-focus", action="store_true")
focus_display_parser.set_defaults(func=focus_display_direction)

send_to_display_parser = subparsers.add_parser("send-to-display")
send_to_display_parser.add_argument("direction", choices=['north', 'south', 'east', 'west'])
send_to_display_parser.add_argument("--no-focus", action="store_true")
send_to_display_parser.set_defaults(func=send_to_display_direction)

change_layout_parser = subparsers.add_parser("change-layout")
change_layout_parser.add_argument("layout", choices=['bsp', 'stack', 'float'])
change_layout_parser.set_defaults(func=change_layout)

change_layout_parser = subparsers.add_parser("window")
change_layout_parser.add_argument("toggle", choices=['float', 'zoom-parent', 'zoom-fullscreen', 'native-fullscreen'])
change_layout_parser.set_defaults(func=window_options)



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
