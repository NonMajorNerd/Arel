from time import time
import tcod as libtcod

from enum import Enum

from tcod import constants

from game_states import GameStates
 
from menus import character_screen, inventory_menu, level_up_menu
from equipment_slots import EquipmentSlots

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
                             '{0}: {1}/{2}'.format(name, int(value), int(maximum)))

def render_tooltip(x, y, text):
    
    if len(text) + 2 > 58:
        print(text)
        raise Exception("Tooltip text is too long. Must be 58 characters or less, string was " + (str(len(text))) + " characters.")
    
    ttcon = libtcod.console.Console(len(text)+4, 3)
    libtcod.console_set_default_background(ttcon, libtcod.Color(102,102,102))
    libtcod.console_set_default_foreground(ttcon, libtcod.black)
    
    libtcod.console_clear(ttcon)
    
    libtcod.console_print_ex(ttcon, 0, 0, libtcod.BKGND_NONE, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(ttcon, len(text)+3, 0, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(ttcon, 0, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(ttcon, len(text)+3, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
    libtcod.console_print_ex(ttcon, 0, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    libtcod.console_print_ex(ttcon, len(text)+3, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    for tx in range(1, len(text)+3):
        libtcod.console_print_ex(ttcon, tx, 0, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        libtcod.console_print_ex(ttcon, tx, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(205))

    libtcod.console_set_default_foreground(ttcon, libtcod.white)    
    libtcod.console_print_ex(ttcon, 2, 1, libtcod.BKGND_NONE, libtcod.LEFT, str(text).capitalize())
    
    while ((y-3) < 1): y=+1
    while ((x+len(text)+4) > 59): x-=1
    libtcod.console_blit(ttcon, 0, 0, 0, 0, 0, x, y)

def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, options_tutorial_enabled, game_state, names_list, colors_list, tick, tick_speed):
               
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
        draw_entity(con, entity, fov_map, game_map, tick, tick_speed)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    
    if game_state == GameStates.KEYTARGETING:
        if player.y >= game_map.height/2: #player on bottom half of the screen
            (tx, ty) = (58, 2)
        else: #player on top half of the map
            (tx, ty) = (58, 32)
            
        libtcod.console_set_default_background(0, libtcod.lighter_blue)
        libtcod.console_set_default_foreground(0, libtcod.black)
                
        libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Press [esc] to exit targeting.")
                    
    #print mouse x/y
    #libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT, (str(mouse.cx) + "," + str(mouse.cy)))
    
    if options_tutorial_enabled:
            MAP_HEIGHT = game_map.height
            MAP_WIDTH = game_map.width
            
            if game_map.dungeon_level < 3:
                libtcod.console_set_default_background(0, libtcod.lighter_yellow)
                libtcod.console_set_default_foreground(0, libtcod.black)
                
                if player.y >= MAP_HEIGHT/2: #player on bottom half of the screen
                    (tx, ty) = (58, 2)
                else: #player on top half of the map
                    (tx, ty) = (58, MAP_HEIGHT-2)
                    
                if game_state != GameStates.KEYTARGETING:
                    if player.turn_count < 4:
                        libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Use the numpad or arrow keys to move.")
                   
                    elif player.turn_count < 9:
                        libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "You can move into creatures to attack with a melee ")
                        libtcod.console_print_ex(0, tx, ty+1, libtcod.BKGND_SET, libtcod.RIGHT, "weapon, or press [f] to fire a ranged weapon.")
                        
                    elif player.turn_count < 14:
                        libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Press [x] to examine creatures or items on the ground.")
                        
                    else:
                 
                        for ent in entities:
                           if not ent.name == "Player":
                               if ent.x == player.x and ent.y == player.y:
                                    if ent.name == "stairs":
                                        libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Press [Enter] to go down the stairs.")
                                    elif ent.item:
                                        if not game_map.tiles[ent.x][ent.y].door:
                                            libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Press [g] to grab an item.")
                                    
                                            
                        myneighbors = [(-1, -1), (0, -1), (1, -1),
                                     (-1, 0), (1, 0),
                                     (-1, 1), (0, 1), (1, 1)]
                                     
                        for dx, dy in myneighbors:
                            tdx, tdy = player.x + dx, player.y + dy
                            if game_map.tiles[tdx][tdy].door:
                                if game_map.tiles[tdx][tdy].block_sight:
                                    libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Move into a closed door to open it.")
                                else:  
                                    libtcod.console_print_ex(0, tx, ty, libtcod.BKGND_SET, libtcod.RIGHT, "Press [c] and then a direction to close an open door.")
                                                       
    # Print the game messages, one line at a time
    # y = 1
    # for message in message_log.messages:
    #     libtcod.console_set_default_foreground(panel, message.color)
    #     libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
    #     y += 1

    #health bar
    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    #score tracker           
    libtcod.console_print_ex(panel, 1, 2, libtcod.BKGND_NONE, libtcod.LEFT, "Score: " + str(player.score))           
    # libtcod.console_print_ex(panel, 1, 3, libtcod.BKGND_NONE, libtcod.LEFT,
    #                          'Dungeon level: {0}'.format(game_map.dungeon_level))
    # libtcod.console_print_ex(panel, 1, 4, libtcod.BKGND_NONE, libtcod.LEFT,
    #                          'Turn : {0}'.format(player.turn_count))

    #print condition icons       
    if len(player.conditions) > 0:
        ind = 0
        for condition in player.conditions:
            if condition.active:
                libtcod.console_print_ex(panel, 1+ind, 2, libtcod.BKGND_SET, libtcod.LEFT, condition.char)
                libtcod.console_set_char_background(panel, 1+ind, 2, condition.bgcolor, libtcod.BKGND_SET)
                libtcod.console_set_char_foreground(panel, 1+ind, 2, condition.fgcolor)
                ind += 1
               
    #timeline
    libtcod.console_set_default_foreground(panel, libtcod.dark_gray)
    libtcod.console_print_ex(panel, 22, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(195) )     #195 >
    libtcod.console_print_ex(panel, 58, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(180) )     #180 <
    for x in range(23, 58):
        libtcod.console_print_ex(panel, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(196) )  #196 -

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, 23, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(player.char) )     #player char
    
    turn_order = []
    for ent in entities:
        if not ent.name == player.name and ent.ai and libtcod.map_is_in_fov(fov_map, ent.x, ent.y):
            temp_enemy_timer = ent.fighter.timer + ent.fighter.speed
            while temp_enemy_timer >= player.fighter.speed:
                turn_order.append(ent)
                temp_enemy_timer -= player.fighter.speed

    x = 25
    for ent in turn_order:
        if x < 58:
            libtcod.console_print_ex(panel, x, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(ent.char+1))
            x = x + 2  

    #check for timeline highlighting
    if mouse.cy == 37:
        if mouse.cx >= 25 and mouse.cx <= 57:
            timeline_index = (mouse.cx - 25)
            if mouse.cx %2 == 0: timeline_index -= 1
            timeline_index = int(timeline_index / 2)
        else:
            timeline_index = 99

        if timeline_index <= len(turn_order)-1 and tick%tick_speed<2:
            ent = turn_order[timeline_index]
            libtcod.console_set_default_foreground(0, libtcod.lighter_yellow)
            libtcod.console_print_ex(0, ent.x, ent.y, libtcod.BKGND_NONE, libtcod.LEFT, chr(ent.char))

            # TODO :: Look at this... this code was an attempt to highlight each occurance of a highlighted creature in the timeline
            #so if you highlight a rat, and he gets two turns, I wanted both of his sprites on the timeline to highlight.
            #didn't work, but it did manage to highlight the specific sprite you were hovering over on the timeline.

            # for e in turn_order:
            #     if e == turn_order[timeline_index]:
            #         ex = 25 + (2*timeline_index)
            #         libtcod.console_set_default_foreground(panel, libtcod.lighter_yellow)
            #         libtcod.console_print_ex(panel, ex, 1, libtcod.BKGND_NONE, libtcod.LEFT, chr(ent.char))

    for ent in entities:
        if libtcod.map_is_in_fov(fov_map, ent.x, ent.y) and ent.x == mouse.cx and ent.y == mouse.cy and ent.name != "Targeter" and ent.name != "Player":
                if ent.fighter:
                    #print a context menu for the lil guy
                    context_menu(game_map.width, game_map.height, ent, names_list)
                    break
                else:
                    render_tooltip(ent.x+1, ent.y-1, ent.name)


    if game_state == GameStates.KEYTARGETING:
        targeter = None
        for ent in entities:
            if ent.name == 'Targeter':
                targeter = ent
        if not targeter == None:
            #libtcod.console_set_default_foreground(panel, libtcod.light_gray)
            libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                                 get_all_at(targeter.x, targeter.y, entities, fov_map, game_map, names_list))
            for ent in entities:
                if libtcod.map_is_in_fov(fov_map, ent.x, ent.y) and ent.x == targeter.x and ent.y == targeter.y and ent.name != "Targeter" and ent.name != "Player":
                    if ent.fighter:
                        #print a context menu for the lil guy
                        context_menu(game_map.width, game_map.height, ent, names_list)
                        break
                    else:
                        render_tooltip(ent.x+1, ent.y-1, ent.name)

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

def context_menu(gmw, gmh, entity, names_list):

    if not entity.fighter:
        print("Context menu called, but entity " + entity.name + " has no fighter component.")
        return

    h = 8
    if len(entity.conditions) > 0: h += 2
    if entity.equipment and len(entity.equipment.list) > 0: h += 2
    
    w = len(names_list[entity.name]) + 4
    if w < 9: w = 9
    #if w%2 != 0: w-=1
    
    x = entity.x + 1
    if entity.x + w + 1 > gmw: x = entity.x - w - 1
    
    y = entity.y - h
    if entity.y - h < 1: y = entity.y
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    #print UI elements
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)

    #background
    for iy in range (y, y+h+1):
        for ix in range (x, x+w+2):
            libtcod.console_print_ex(0, ix, iy, libtcod.BKGND_SET, libtcod.LEFT, " ")

    #lines
    for ix in range(x, x+w+2):
        libtcod.console_print_ex(0, ix, y, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        libtcod.console_print_ex(0, ix, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        
    for iy in range(y, y+h+1):
        libtcod.console_print_ex(0, x, iy, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        libtcod.console_print_ex(0, x+w+1, iy, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
          
    #corners
    libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(0, x+w+1, y, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, x, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, x+w+1, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
    printy = y+1
    #print entity info
    strname = chr(entity.char) + " " + names_list[entity.name]
    libtcod.console_set_default_foreground(0, libtcod.white)
    px = x+int(w/2)+1
    libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, strname) 
    
    libtcod.console_set_default_foreground(0, entity.color)
    
    charx = px - int(len(strname)/2)
    #if len(strname)%2 != 0: charx -= 1
    
    libtcod.console_print_ex(0, charx, y+1, libtcod.BKGND_SET, libtcod.CENTER, chr(entity.char)) 
    #print("x:" + str(x) + " y:" + str(y) + " w:" + str(w) + " (" + str(int(w/2)) + ") h:" + str(h) + " px" + str(px) + " cx:" + str(charx) + " modlen:" + str(len(strname)%2))
    
    printy += 1
    strhealth = "OOPS"
    #print(str(entity.fighter.hp / entity.fighter.max_hp))
    if entity.fighter.hp > entity.fighter.max_hp * 0.90:
        libtcod.console_set_default_foreground(0, libtcod.dark_green)
        strhealth = "Healthy"
    elif  entity.fighter.hp > entity.fighter.max_hp * 0.70:
        libtcod.console_set_default_foreground(0, libtcod.lime)
        strhealth = "Bruised"
    elif  entity.fighter.hp > entity.fighter.max_hp * 0.50:
        libtcod.console_set_default_foreground(0, libtcod.light_yellow)
        strhealth = "Wounded"
    elif  entity.fighter.hp > entity.fighter.max_hp * 0.30:
        libtcod.console_set_default_foreground(0, libtcod.amber)
        strhealth = "Bloody"
    else:
        libtcod.console_set_default_foreground(0, libtcod.light_flame)
        strhealth = "Maimed"
    libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, strhealth)  
    printy += 2
    
    l = len(entity.conditions)
    if l > 0:
        if l == 1:
            libtcod.console_set_default_foreground(0, entity.conditions[0].fgcolor)
            libtcod.console_set_default_background(0, entity.conditions[0].bgcolor)
            libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, entity.conditions[0].char)
            
        if l ==2:
            libtcod.console_set_default_foreground(0, entity.conditions[0].fgcolor)
            libtcod.console_set_default_background(0, entity.conditions[0].bgcolor)
            libtcod.console_print_ex(0, px-1, printy, libtcod.BKGND_SET, libtcod.CENTER, entity.conditions[0].char)
            
            libtcod.console_set_default_foreground(0, entity.conditions[1].fgcolor)
            libtcod.console_set_default_background(0, entity.conditions[1].bgcolor)
            libtcod.console_print_ex(0, px+1, printy, libtcod.BKGND_SET, libtcod.CENTER, entity.conditions[1].char)
            
        printy += 2    
            
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, screen_lightgray)
    strpower = "POW  " + str(entity.fighter.power)
    if entity.fighter.power < 10: strpower = "POW  0" + str(entity.fighter.power)
    libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, strpower)
    printy += 1
    
    strdef = "DEF  " + str(entity.fighter.defense)
    if entity.fighter.defense < 10: strdef = "DEF  0" + str(entity.fighter.defense)
    libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, strdef)
    printy += 1
    
    strspeed = "SPD  " + str(entity.fighter.speed)
    if entity.fighter.speed < 10: strspeed = "SPD  0" + str(entity.fighter.speed)
    libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, strspeed)
    printy += 2
    
    if entity.equipment and len(entity.equipment.list) > 0:
        libtcod.console_set_default_foreground(0, screen_blue)
        for eq in entity.equipment.list:
            if eq.equippable.slot == EquipmentSlots.MAIN_HAND:
                streq = chr(eq.char) + " " + names_list[eq.name]
                streq[:w-2]
                libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, streq)
                printy += 1
            elif eq.equippable.slot == EquipmentSlots.OFF_HAND:
                streq = chr(eq.char) + " " + names_list[eq.name]
                streq[:w-2]
                libtcod.console_print_ex(0, px, printy, libtcod.BKGND_SET, libtcod.CENTER, streq)
                printy += 1
    
def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)


def draw_entity(con, entity, fov_map, game_map, tick, tick_speed):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        charmod = 0
        if entity.ai or entity.name == "Player":
            mod = tick % tick_speed
            if mod < 2: charmod = 1
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, (entity.char+charmod), libtcod.BKGND_NONE)


def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
