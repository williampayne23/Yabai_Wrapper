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
    yabai_tools.window_toggle(args.toggle, window_id=args.window_id)

def search(args):
    output = {
        "items" : items
    }
    print(json.dumps(output))

def window_list(args):
    if args.open_alfred:
        os.system('osascript -e \'tell application id "com.runningwithcrayons.Alfred" to run trigger "window_list" in workflow "com.alfredapp.yabai_tools"\'')
        return
    windows = []
    for window in yabai_tools.get_windows():
        windows.append(make_item(window['title'], window['app'], "window-options --open-alfred --window-id {window_id} s".format(window_id=window['id']), app_icon={'title': window['app'], "pid": window['pid']}))

    print(json.dumps({"items": windows}))


def window_options_menu(args):
    if args.open_alfred:
        os.system('osascript -e \'tell application id "com.runningwithcrayons.Alfred" to run trigger "window_actions" in workflow "com.alfredapp.yabai_tools" with argument "{window_id}"\''.format(window_id=args.window_id))
        return
    window_id = "" if (args.window_id == None) else "--window-id " + args.window_id
    arg = lambda action : "window {action} ".format(action=action, window_id=args.window_id) + window_id
    window_options = [
            make_item("Float", "Float this window", arg("float"), icon="window-restore-regular"),
            make_item("Zoom Parent", "Zoom to the parent window", arg("zoom-parent"), icon="expand-alt-solid"),
            make_item("Zoom Fullscreen", "Fill the screen", arg("zoom-fullscreen"), icon="expand-alt-solid"),
            make_item("Native Fullscreen", "Full Screen Mode", arg("native-fullscreen"), icon="expand-alt-solid"),
            make_item("Bordered", "Toggle Bordered", arg("border"), icon="Square"),
    ]
    output = {
        "items" : window_options
    }
    print(json.dumps(output))

def make_item(title, subtitle, arg, uid=None, item_type=None, autocomplete=None, icon="", app_icon={}):
    if autocomplete == None:
        autocomplete=title
    
    if not os.path.isdir('./icons'):
        path = "./icons"
        access_rights = 0o755
        os.mkdir(path, access_rights)

    if icon!="":
        path = "./icons/{icon}.png".format(icon=icon)
        if not os.path.isfile(path):
            response = requests.get("https://github.com/williampayne23/Yabai_Wrapper/raw/41005119f0677e0b7d3a7a228bc9ad7bf038c56a/icons/" + icon)
            file = open(path, "wb")
            file.write(response.content)
            file.close()
        icon = {
            "path":path
        }
    elif app_icon!={}:
        path = "./icons/{icon}.png".format(icon=str(app_icon['title']))
        if not os.path.isfile(path):
            os.system('node icon_getter.js ' + str(app_icon['pid']) + ' ' + path)
        icon = {
            "path":path
        }
    else:
        icon = {}

    return (
        {
            "uid": uid,
            "type": item_type,
            "title": title,
            "subtitle": subtitle,
            "arg": arg,
            "autocomplete": autocomplete,
            "icon": icon
        })

def add_to_menu(title, subtitle, arg, uid=None, item_type=None, autocomplete=None, icon="", app_icon={}):
    items.append(make_item(title, subtitle, arg, uid=uid, item_type=item_type, autocomplete=autocomplete, icon=icon, app_icon=app_icon))


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
add_to_menu("grid layout", "Switch to grid layout", "change-layout bsp", icon="border-all-solid")
add_to_menu("stack layout", "Switch to stack layout", "change-layout stack", icon="layer-group-solid")
add_to_menu("free layout", "Switch to free layout", "change-layout float", icon="window-restore-regular")



window_parser = subparsers.add_parser("window", help="Toggle choices for the given window")
window_parser.add_argument("toggle", choices=['float', 'zoom-parent', 'zoom-fullscreen', 'native-fullscreen', 'border'])
window_parser.add_argument("--window-id")
window_parser.set_defaults(func=window_options)
add_to_menu("window float", "Ignore yabai for this window", "window float", icon="window-restore-regular")

change_layout_parser = subparsers.add_parser("search", help="The manager for the Alfred Search Workflow")
change_layout_parser.add_argument("search")
change_layout_parser.set_defaults(func=search)

window_options_parser = subparsers.add_parser("window-options", help="The manager for the Alfred Window Workflow")
window_options_parser.add_argument("--window-id")
window_options_parser.add_argument("--open-alfred", action="store_true")
window_options_parser.set_defaults(func=window_options_menu)
window = yabai_tools.get_current_window()
add_to_menu("Window options", "Show Options For "+ window['app'], 'window-options --open-alfred', app_icon={"pid": window['pid'], "title":window['app']})

window_list_parser = subparsers.add_parser("window-list")
window_list_parser.add_argument("--window-id")
window_list_parser.add_argument("--open-alfred", action="store_true")
window_list_parser.set_defaults(func=window_list)
add_to_menu("Window list", "Show Window List", 'window-list --open-alfred')

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
