import os, json, sys
from yabai_tools import *

def initiate(direction):
    next_bordered = id_in_direction(get_main_id(), direction)
    if (next_bordered == None):
        send_to_display(direction)
        return
    toggle_bordered(next_bordered)
    

def move(direction, current_id):
    next_bordered = id_in_direction(current_id, direction)
    if(next_bordered == None):
        send_to_display(direction)
        toggle_bordered(current_id)
        return
    toggle_bordered(next_bordered)
    toggle_bordered(current_id)

def end(current_id):
    toggle_bordered(current_id)
    swap_to(current_id)

def get_bordered():
    output = get_windows()
    filtered = list(filter(lambda w: w['border'] == 1, output))
    if (len(filtered) == 1):
        return filtered[0]['id']
    else:
        return -1

def swap_select(direction, key_mod=False):
    bordered = get_bordered()
    if(direction == None or direction == 'swap'):
        if (bordered != -1):
            end(bordered)
    else:
        if (bordered == -1):
            initiate(direction)
            if(key_mod):
                dirname = os.path.dirname(__file__)
                filename = os.path.join(dirname, 'yabaiEndSwitch.scpt')
                os.system('osascript ' + filename)
        else:
            move(direction, bordered) 
