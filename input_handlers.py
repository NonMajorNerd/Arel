import tcod as libtcod

from game_states import GameStates
from ammo_functions import Fire_And_Preference

def handle_keys(key, game_state):
    if game_state == GameStates.PLAYERS_TURN:
        return handle_player_turn_keys(key)
    elif game_state == GameStates.PLAYER_DEAD:
        return handle_player_dead_keys(key)
    elif game_state == GameStates.KEYTARGETING:
        return  player_pick_dir(key, strkey='move')
    elif game_state == GameStates.TARGETING:
        return handle_targeting_keys(key)
    #elif game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
    #    return handle_inventory_keys(key)
    elif game_state == GameStates.LEVEL_UP:
        return handle_level_up_menu(key)
    elif game_state == GameStates.CHARACTER_SCREEN:
        return handle_character_screen(key)
    elif game_state == GameStates.KICKING:
        return  player_pick_dir(key, strkey='kick')
    elif game_state == GameStates.CLOSING:
        return  player_pick_dir(key, strkey='close')
    elif game_state == GameStates.FIRING:
        return  player_pick_dir(key, strkey='fire')
        
    return {}

def player_pick_dir(key, strkey='None'):

    key_char = chr(key.c)

    # Movement keys
    if key.shift:
        if key.vk == libtcod.KEY_UP:
            return {strkey: (1, -1)}
        elif key.vk == libtcod.KEY_DOWN:
            return {strkey: (-1, 1)}
        elif key.vk == libtcod.KEY_LEFT:
            return {strkey: (-1, -1)}
        elif key.vk == libtcod.KEY_RIGHT:
            return {strkey: (1, 1)}
    else:
        if key.vk == libtcod.KEY_KP9:
            return {strkey: (1, -1)}
        elif key.vk == libtcod.KEY_KP1:
            return {strkey: (-1, 1)}
        elif key.vk == libtcod.KEY_KP7:
            return {strkey: (-1, -1)}
        elif key.vk == libtcod.KEY_KP3:
            return {strkey: (1, 1)}
        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            return {strkey: (0, -1)}
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            return {strkey: (0, 1)}
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            return {strkey: (-1, 0)}
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            return {strkey: (1, 0)}


    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_turn_keys(key):
    key_char = chr(key.c)

    # Movement keys
    if key.shift:
        if key.vk == libtcod.KEY_UP:
            return {'move': (1, -1)}
        elif key.vk == libtcod.KEY_DOWN:
            return {'move': (-1, 1)}
        elif key.vk == libtcod.KEY_LEFT:
            return {'move': (-1, -1)}
        elif key.vk == libtcod.KEY_RIGHT:
            return {'move': (1, 1)}
            
        elif key_char == '/': #might be vk
            return {'show_help': True}   
            
    else:
        if key.vk == libtcod.KEY_KP9:
            return {'move': (1, -1)}
        elif key.vk == libtcod.KEY_KP1:
            return {'move': (-1, 1)}
        elif key.vk == libtcod.KEY_KP7:
            return {'move': (-1, -1)}
        elif key.vk == libtcod.KEY_KP3:
            return {'move': (1, 1)}
        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            return {'move': (0, -1)}
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            return {'move': (0, 1)}
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            return {'move': (-1, 0)}
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            return {'move': (1, 0)}
        elif key_char == 'z' or key.vk == libtcod.KEY_KP5:
            return {'wait': True}
            
    if key_char == 'c':
        return {'close': True}
        
    elif key_char == 'f':
        return {'fire': True}
        
    elif key_char == 'g':
        return {'pickup': True}

    elif key_char == 'k':
        return {'kick': True}

    elif key_char == 'l':
        return {'messagelog': True}

    elif key_char == 'i':
        return {'show_inventory': True}
        
    elif key_char == 'x':
        return {'key_targeting': True}

    elif key_char == 'd':
        return {'show_inventory': True}

    elif key.vk == libtcod.KEY_ENTER or key_char == '>':
        return {'take_stairs': True}

    elif key_char == 's':
        return {'show_character_screen': True}

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the game
        return {'exit': True}

    # No key was pressed
    return {}

def handle_targeting_keys(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_player_dead_keys(key):
    key_char = chr(key.c)

    if key_char == 'i':
        return {'show_inventory': True}
    elif key_char == 'l':
        return {'messagelog': True}
        
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    elif key.vk == libtcod.KEY_ESCAPE:
        # Exit the menu
        return {'exit': True}

    return {}

#def handle_inventory_keys(key):
#    index = key.c - ord('a')
#
#    if index >= 0:
#        return {'inventory_index': index}
#
#    if key.vk == libtcod.KEY_ENTER and key.lalt:
#        # Alt+Enter: toggle full screen
#        return {'fullscreen': True}
#    elif key.vk == libtcod.KEY_ESCAPE:
#        # Exit the menu
#        return {'exit': True}
#
#    return {}

def handle_main_menu(key):
    key_char = chr(key.c)

    if key_char == 'a':
        return {'new_game': True}
    elif key_char == 'b':
        return {'load_game': True}
    elif key_char == 'c' or key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_level_up_menu(key):
    if key:
        key_char = chr(key.c)

        if key_char == 'a':
            return {'level_up': 'hp'}
        elif key_char == 'b':
            return {'level_up': 'str'}
        elif key_char == 'c':
            return {'level_up': 'def'}

    return {}

def handle_character_screen(key):
    if key.vk == libtcod.KEY_ESCAPE:
        return {'exit': True}

    return {}

def handle_mouse(mouse):
    (x, y) = (mouse.cx, mouse.cy)

    if mouse.lbutton_pressed:
        return {'left_click': (x, y)}
    elif mouse.rbutton_pressed:
        return {'right_click': (x, y)}

    return {}
