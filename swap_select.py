import os, json, sys
from yabai_tools import *

dir_path = os.path.dirname(os.path.realpath(__file__)) + '/'


def initiate(direction, follow_focus=True):
    next_bordered = id_in_direction(get_main_id(), direction)
    if (next_bordered == None):
        send_to_display(direction, follow_focus=follow_focus)
        return
    toggle_bordered(next_bordered)
    

def move(direction, current_id, follow_focus=True):
    next_bordered = id_in_direction(current_id, direction)
    if(next_bordered == None):
        send_to_display(direction, follow_focus=follow_focus)
        toggle_bordered(current_id)
        return
    toggle_bordered(next_bordered)
    toggle_bordered(current_id)

def end(current_id, follow_focus=True):
    toggle_bordered(current_id)
    swap_to(current_id, follow_focus=follow_focus)

def get_bordered():
    output = get_windows()
    filtered = list(filter(lambda w: w['border'] == 1, output))
    if (len(filtered) == 1):
        return filtered[0]['id']
    else:
        return -1

def swap_select(direction, follow_focus=True):
    bordered = get_bordered()
    if(direction == None or direction == 'swap'):
        if (bordered != -1):
            end(bordered, follow_focus)
    else:
        if (bordered == -1):
            initiate(direction, follow_focus=follow_focus)
        else:
            move(direction, bordered, follow_focus=follow_focus) 
