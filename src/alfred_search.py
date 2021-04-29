import os, json, requests
import yabai_tools

def window_list(args):
    if args.open_alfred:
        os.system('osascript -e \'tell application id "com.runningwithcrayons.Alfred" to run trigger "window_list" in workflow "com.alfredapp.yabai_tools"\'')
        return
    windows = []
    for window in yabai_tools.get_windows():
        if window['title'] != 'Alfred':
            windows.append(make_item(window['title'], window['app'], "window-options --open-alfred --window-id {window_id}".format(window_id=window['id']), icon=make_app_icon(window['pid'], window['app'])))

    print(json.dumps({"items": windows}))

def search(args):
    items = []
    def add_to_menu(title, subtitle, arg, uid=None, item_type=None, autocomplete=None, icon={}):
        items.append(make_item(title, subtitle, arg, uid=uid, item_type=item_type, autocomplete=autocomplete, icon=icon))
    
    add_to_menu("Grid layout", "Switch to grid layout", "change-layout bsp", icon=make_url_icon("border-all-solid"))
    add_to_menu("Stack layout", "Switch to stack layout", "change-layout stack", icon=make_url_icon("layer-group-solid"))
    add_to_menu("Free layout", "Switch to free layout", "change-layout float", icon=make_url_icon("window-restore-regular"))

    window = yabai_tools.get_current_window()
    if window != None:
        action = "Manage" if window['floating'] else "Float"
        add_to_menu(action, action + " this window", "window float", icon=make_url_icon("window-restore-regular"))
        add_to_menu("Window options", "Show Options For "+ window['app'], 'window-options --open-alfred --window-id ' + str(window['id']), icon=make_app_icon(window['pid'], window['app']))
    
    add_to_menu("Window list", "Show Window List", 'window-list --open-alfred')
    output = {
        "items" : items
    }
    print(json.dumps(output))


def window_options_menu(args):
    if args.open_alfred:
        os.system('osascript -e \'tell application id "com.runningwithcrayons.Alfred" to run trigger "window_actions" in workflow "com.alfredapp.yabai_tools" with argument "{window_id}"\''.format(window_id=args.window_id))
        return
    window = yabai_tools.get_current_window()
    window_id_str = ""
    if args.window_id != None:
        window_id_str = "--window-id " + args.window_id
        window = yabai_tools.get_window(args.window_id)
    arg = lambda action : "window {action} ".format(action=action, window_id=args.window_id) + window_id_str
    window_options = []
    
    window_options.append(make_item("Focus", "Focus on this window", arg("focus"), icon=make_url_icon("window-restore-regular")))
    window_options.append(make_item("Close", "Close this window", arg("close"), icon=make_url_icon("window-restore-regular")))
    window_options.append(make_item("Swap to", "Swap to this window", arg("swap"), icon=make_url_icon("window-restore-regular")))
    action = "Manage" if window['floating'] else "Float"
    window_options.append(make_item(action, action + " this window", arg("float"), icon=make_url_icon("window-restore-regular")))
    window_options.append(make_item("Zoom Parent", "Zoom to the parent window", arg("zoom-parent"), icon=make_url_icon("expand-alt-solid")))
    window_options.append(make_item("Zoom Fullscreen", "Fill the screen", arg("zoom-fullscreen"), icon=make_url_icon("expand-alt-solid")))
    window_options.append(make_item("Native Fullscreen", "Full Screen Mode", arg("native-fullscreen"), icon=make_url_icon("expand-alt-solid")))
    
    action = "Unborder" if window['border'] else "Border"
    window_options.append(make_item(action, action + " this window", arg("border"), icon=make_url_icon("Square")))
    output = {
        "items" : window_options
    }
    print(json.dumps(output))

def make_item(title, subtitle, arg, uid=None, item_type=None, autocomplete=None, icon={}):
    if autocomplete == None:
        autocomplete=title
    
    if not os.path.isdir('./icons'):
        path = "./icons"
        access_rights = 0o755
        os.mkdir(path, access_rights)

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


def make_app_icon(pid, title):
    path = "./icons/{icon}.png".format(icon=str(title))
    if not os.path.isfile(path):
        os.system('node icon_getter.js ' + str(pid) + ' ' + path)
    icon = {
        "path":path
    }
    return icon

def make_url_icon(icon_url):
    path = "./icons/{icon}.png".format(icon=icon_url)
    if not os.path.isfile(path):
        response = requests.get("https://raw.githubusercontent.com/williampayne23/Yabai_Wrapper/master/icons/" + icon_url + '.png')
        file = open(path, "wb")
        file.write(response.content)
        file.close()
    icon = {
        "path":path
    }