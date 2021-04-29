import os, json

def careful_load_json(data):
    try:
        return json.loads(data)
    except:
        return None

def get_windows():
    stream = os.popen('yabai -m query --windows')
    return careful_load_json(stream.read())

def get_current_window():
    stream = os.popen('yabai -m query --windows --window')
    return careful_load_json(stream.read())

def get_window(id):
    stream = os.popen('yabai -m query --windows --window ' + str(id))
    return careful_load_json(stream.read())

def get_main_id():
    output = get_current_window()
    if(output == None):
        return None
    try:
        return json.loads(output)['id']
    except:
        return None

def close_window(id):
    os.system('yabai -m window ' + id + ' --close')

def window_toggle(toggle, window_id=None):
    if window_id == None or window_id=="None":
        os.system('yabai -m window --toggle ' + toggle)
    else:
        os.system('yabai -m window ' + window_id + ' --toggle ' + toggle)

#implmented in terminal wrapper   
def change_layout(layout):
    """
    Changes system layout to layout
    """
    os.system('yabai -m config layout ' + layout)

def toggle_bordered(id):
    os.system('yabai -m window ' + str(id) + ' --toggle border')

def swap_to(id):
    os.system('yabai -m window --swap '+ str(id))
#implmented in terminal wrapper
def focus_direction(direction):
    target_id = id_in_direction(get_main_id(), direction)
    if(target_id == None):
        focus_display(direction)
    else:
        focus_to(target_id)
#implmented in terminal wrapper
def focus_display(direction):
    """
    Focusses on the display in direction
    """
    os.system('yabai -m display --focus ' + direction)

def focus_to(id):
    os.system('yabai -m window --focus ' + str(id))

#implmented in terminal wrapper
def send_to_display(direction):
    main_id = get_main_id()
    os.system('yabai -m window --display ' + direction)
    focus_to(main_id)

def id_in_direction(start, direction):
    def get_edge(window, direction):
        if (direction == 'east'):
            return window['frame']['x'] + window['frame']['w']
        elif (direction == 'west'):
            return window['frame']['x']
        elif (direction == 'north'):
            return window['frame']['y']
        elif (direction == 'south'):
            return window['frame']['y'] + window['frame']['h']

    def get_opposite_direction(direction):
        pairs = {
            'east' : 'west',
            'west' : 'east',
            'south': 'north',
            'north': 'south'
        }
        return pairs[direction]

    def get_sign(direction):
        dirs = {
            'east' : +1,
            'west' : -1,
            'south': +1,
            'north': -1
        }
        return dirs[direction]

    def get_perp_axis(direction):
        axes = {
            'east' : 'y',
            'west' : 'y',
            'south': 'x',
            'north': 'x'
        }
        return axes[direction]

    windows = get_windows()
    visible = filter(lambda x: x['visible'], windows)

    window = get_current_window()
    otherWindows = list(filter(lambda window: window['id'] != start, visible))
    if (window == None or len(otherWindows) == 0):
        return None
    
    window_edge = get_edge(window, direction)
    closest_windows = []
    smallest = float('inf')
    for w in otherWindows:
        distance = (get_edge(w, get_opposite_direction(direction)) - window_edge) * get_sign(direction) + 10
        if (distance > 0):
            if (distance < smallest):
                smallest = distance
                closest_windows = [w]
            elif (distance == smallest):
                closest_windows.append(w)
    if(len(closest_windows) > 0):
        closest_windows.sort(key=lambda w: abs(w['frame'][get_perp_axis(direction)] - window['frame'][get_perp_axis(direction)]))
        return closest_windows[0]['id']
    else:
        return None