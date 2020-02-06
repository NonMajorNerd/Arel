import tcod as libtcod

from enum import Enum

from game_states import GameStates
 
from menus import character_screen, inventory_menu, level_up_menu


class RenderOrder(Enum):
    JUNK = 1
    STAIRS = 2
    CORPSE = 3
    ITEM = 4
    ACTOR = 5
    TARGETING = 6

def get_names_under_mouse(mouse, entities, fov_map, names_list):
    (x, y) = (mouse.cx, mouse.cy)

    names = [names_list[entity.name] for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()
    
def get_all_at(x, y, entities, fov_map, game_map, names_list):
    
    if not libtcod.map_is_in_fov(fov_map, x, y):
        names = "???"
    else:
        if game_map.tiles[x][y].door:
            tiles = 'Door'
        elif game_map.tiles[x][y].block_sight:
            tiles = 'Wall'
        else:
            tiles = 'Floor'  
    
        names = ""
        names = [names_list[entity.name] for entity in entities
                 if entity.x == x and entity.y == y and not entity.name == "Targeter"]  
            
        names = ', '.join(names)
        names.capitalize()
        
    if names == "???":
        return names
    else:
        if not names == "":
            tiles = tiles + ", " + names
     
    return tiles


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))

def render_tooltip(x, y, text):
    if 0 > x > self.width or 0 > y > self.height:
        raise Exception("Render tooltip range is out of screen area. (" + str(x) + "," + str(y) + ")")
    
    if len(text) + 2 > 58:
        print(text)
        raise Exception("Tooltip text is too long. Must be 58 characters or less, string was " + (str(len(text))) + " characters.")
    
    ttcon = libtcod.console.Console(len(text)+2, 3)
    libtcod.console_set_default_background(ttcon, libtcod.Color(102,102,102))
    libtcod.console_set_default_foreground(ttcon, libtcod.black)
    
    libtcod.console_clear(ttcon)
    
    libtcod.console_print_ex(ttcon, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(ttcon, len(text)+1, 0, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(ttcon, 0, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(ttcon, len(text)+1, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
    libtcod.console_print_ex(ttcon, 0, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    libtcod.console_print_ex(ttcon, len(text)+1, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    for tx in range(1, len(text)+1):
        libtcod.console_print_ex(ttcon, tx, 0, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        libtcod.console_print_ex(ttcon, tx, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        
    libtcod.console_print_ex(ttcon, 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, str(text))
    
    libtcod.console_blit(ttcon, 0, 0, 0, 0, 0, x, y)

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state, names_list):
               
    if fov_recompute:
    # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                door = game_map.tiles[x][y].door        
                wall = game_map.tiles[x][y].block_sight
                    
                if door:
                    libtcod.console_set_char_foreground(con, x, y, (255,255,255))
                    libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                    libtcod.console_set_char(con, x, y, game_map.tiles[x][y].door.char)
                        
                elif wall:
                    #assign characters based on blitmap
                    if game_map.blitmap[x][y] in [10]:
                        #east-west walls
                        
                        if game_map.tiles[x][y-1].block_sight == False and game_map.tiles[x][y+1].empty_space:
                            #floor above, empty space below
                            libtcod.console_set_char_background(con, x, y, (0,0,0), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                        
                        elif (game_map.tiles[x][y-1].empty_space and game_map.tiles[x][y+1].block_sight == False) or  (game_map.tiles[x][y-1].block_sight == False and game_map.tiles[x][y+1].block_sight == False):
                            #empty space above, and floor below or floor above, floor below
                            libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))

                        libtcod.console_set_char(con, x, y, 223)

                    elif game_map.blitmap[x][y] in [0, 1, 2, 8, 11]:
                        if game_map.tiles[x][y+1].empty_space:
                            libtcod.console_set_char_background(con, x, y, (0,0,0), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))                            
                        else:
                            libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                            
                        libtcod.console_set_char(con, x, y, 223)
                
                    elif game_map.blitmap[x][y] in [3, 9]:
                        #bottom left, bottom right corners            
                        if game_map.tiles[x][y+1].empty_space:
                            libtcod.console_set_char_background(con, x, y, (0,0,0), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                        else:
                            libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)
                            libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                            
                        libtcod.console_set_char(con, x, y, 223)
   
                    elif game_map.blitmap[x][y] in [4, 5, 6, 7, 12, 13, 14, 15]:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, colors.get('light_wall'))
                        libtcod.console_set_char(con, x, y, 218)
                        
                else: #floor    
                    libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)
                
                if visible:
                    game_map.tiles[x][y].explored = True       
                else:
                    if game_map.tiles[x][y].explored: #explored, not visible
                        bgcolor = (libtcod.console_get_char_background(con,x,y)* .33)
                        fgcolor = (libtcod.console_get_char_foreground(con,x,y)* .33)
                    
                        libtcod.console_set_char_background(con, x, y, bgcolor, libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, fgcolor)
                    else:
                        libtcod.console_set_char_background(con, x, y, (0,0,0), libtcod.BKGND_SET)
                        libtcod.console_set_char_foreground(con, x, y, (0,0,0))
                        
    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)
                
    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    
    #print mouse x/y
    #libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, (str(mouse.cx) + "," + str(mouse.cy)))

    # Print the game messages, one line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Dungeon level: {0}'.format(game_map.dungeon_level))
    libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
                             'Turn : {0}'.format(player.turn_count))
                             
    #print condition icons       
    if len(player.conditions) > 0:
        ind = 0
        for condition in player.conditions:
            if condition.active:
                libtcod.console_print_ex(panel, 1+ind, 2, libtcod.BKGND_SET, libtcod.LEFT, condition.char)
                libtcod.console_set_char_background(panel, 1+ind, 2, condition.bgcolor, libtcod.BKGND_SET)
                libtcod.console_set_char_foreground(panel, 1+ind, 2, condition.fgcolor)
                ind += 1
               
    
    if game_state == GameStates.KEYTARGETING:
        targeter = None
        for ent in entities:
            if ent.name == 'Targeter':
                targeter = ent
        if not targeter == None:
            libtcod.console_set_default_foreground(panel, libtcod.light_gray)
            libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                                 get_all_at(targeter.x, targeter.y, entities, fov_map, game_map, names_list))

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map, names_list))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state == GameStates.PLAYERS_TURN:
        if len(player.conditions) > 0:
            if mouse.cy == 35: #the row where status icons are displayed
                if mouse.cx > 0 and mouse.cx <= len(player.conditions):
                    render_tooltip(mouse.cx+1,36,player.conditions[mouse.cx-1].tooltip)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
