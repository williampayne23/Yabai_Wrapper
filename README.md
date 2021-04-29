# Yabai Wrapper

A python wrapper for yabai with some more advanced features.

Specifically window swap selection, which lets me select a window by holding `ctrl-shift` and the arrow keys and then when I release `ctrl-shift` the selected window swaps with the focussed window.

![this](resources/window_select.gif)

Selecting and focussing on windows works across displays which isn't normally included in yabai. The selecting and focussing functionality moves across displays seamlessly.


## Installation

If you haven't already [install homebrew](https://brew.sh)

Open terminal and install the wrapper

```'shell'
brew install williampayne23/utilities/yabai_wrapper --build-from-source
```

If you haven't already you need to set yabai up to start on boot

```'shell'
brew services start yabai
```

### Optional, a few Yabai extras:

You can mess with your yabai settings by editing the hidden .yabairc file in your home directory (/User/yourusername)

Open that file by typing 
```
open -a TextEdit filename
```

Then copy the following into the file
```
#Tells yabai to manage windows whenever you restart your Mac 
yabai -m config layout bsp
#These tell yabai not to manage windows which can't be resized (such as System Preferences windows)
yabai -m signal --add event=window_created label="Floating Windows" action='yabai -m query --windows --window $YABAI_WINDOW_ID | jq -er ".resizable == 0 and .floating == 0" && yabai -m window $YABAI_WINDOW_ID --toggle float'
yabai -m signal --add event=window_created label="Floating Windows" action='yabai -m query --windows --window $YABAI_WINDOW_ID | jq -er ".resizable == 0 and .floating == 0" && yabai -m window $YABAI_WINDOW_ID --toggle float'
```

### If you'd like to use my SKHD (key binds)

[Install SKHD](https://github.com/koekeishiya/skhd) if you haven't already

Then copy [this file](resources/yabai_wrapper_skhdrc) into your skhdrc (usually kept in /Users/yourusername/.skhdrc)

### If you'd like to use the Alfred workflow

Add [this alfred workflow](resources/yabai_tools.alfredworkflow) you'll need to have [Alfred installed](https://www.alfredapp.com/help/getting-started/install/) and pay for Alfred's powerpack to use workflows

![alfred](resources/alfred.gif)

## Usage
### Key Commands

[I've pulled the below into a cheetsheet here](resources/Key_Commands_Cheetsheet.md)

If you use the SKHD configuration provided you get only a few key commands

`arrow = up-arrow | down-arrow | left-arrow | right-arrow `

`carret = < | > `

| Command               | Result                         |
| ----------------------|-------------------------------:|
| `ctrl-arrow`            | Focus on window in direction |
| `ctrl-shift-arrow`      | Select window in direction for swapping (On release of `ctrl-shift` selected window swaps with the current window)|
| `ctrl-alt-arrow`        | Focus on space in direction |
| `ctrl-alt-shift-arrow`  | Send Window to space in direction |
| `ctrl-carret`           | Focus on desktop in direction |
| `ctrl-shift-carret`     | Send window to desktop in direction |
| `ctrl-x`                | Current window fills the desktop |
| `ctrl-shift-carret`     | Current window covers parent window |

To summmarise a memorable way

| Modifier | Effect |
| :------- | -----: |
| `ctrl`   | Always use (how we know it's for window control) |
| `arrow`  | Direction for Windows and Spaces |
| `shift`  | If `shift` is down you move windows if not you move focus |
 | `alt` | For controlling spaces |
| `carret` | Jumping between desktops |

### Alfred Menu

By default the Alfred Menu opens with the keyword `y` for yabai
You can also perform actions on particular windows by typing `yws` for yabai windows.

### Command Line

The wrapper is exposed as `yabai_wrapper` and has a few commands:


```
yabai_wrapper focus (north|south|east|west)
```

Moves focus in direction (unlike yabai this works across displays)

```
yabai_wrapper swap-select (north|south|east|west) (--key-mod)
```

Selects in the given direction, if --key-mod is flagged it will assume the `ctrl-shift` keys are down and trigger a swap when it next sees they are not

```
yabai_wrapper swap-select (swap)
```

Will swap the current window with the selected window

```
yabai_wrapper focus-display (north|south|east|west)
```

Will focus on the display in the given direction

```
yabai_wrapper send-to-display (north|south|east|west)
```

Will send the focussed window to the display in the given direction

```
yabai_wrapper change-layout (bsp|stack|float)
```

Will change the layout to bsp (grid managed), stack (windows stacked on top of each other), or float (unmanaged)

```
yabai_wrapper window option --window-id id
```

Performs the given option on the window of id `id` if no id is given it performs the option on the current window

| Option | Effect |
|:--|--:|
|`float`| Toggles managing the given window |
|`zoom-parent`| Toggles the window zooming fit itself and it's parent|
|`zoom-fullscreen`| Toggles the window filing the desktop|
|`native-fullsceen`| Toggles native mac fullscreen |
|`border`| Toggles a border on the window |
|`Focus`| Focusses on the given window |
|`close`| Closes the given window |
|`Swap`| Swaps the given window with the currently focussed window|

```
yabai_wrapper search
```

Manages the alfred search

```
yabai_wrapper window-options --window-id id (--open-alfred)
```

Used to generate a menu of options to affect a window of `id` from alfred. The '--open-alfred' flag also opens the search for the given --window-id (used by the alfred workflow)  

```
yabai_wrapper window-list (--open-alfred)
```

Used to generate a list of windows for users to select and manage in alfred. The '--open-alfred' flag also opens the search (used by the alfred workflow) 


