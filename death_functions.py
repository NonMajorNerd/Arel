import libtcodpy as libtcod

from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder


def kill_player(player, game_map, constants):
    player.char = 329
    player.color = (255, 255, 177)

    screen_yellow = libtcod.Color(249,220,92)
    screen_blue = libtcod.light_azure
    screen_red = libtcod.Color(254,95,85)
    screen_purple = libtcod.Color(102,46,155)
    
    SCREEN_WIDTH = 60
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
     
    while True:
        #render the screen. this erases the inventory and shows the names of objects under the mouse.
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_clear(0)
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        libtcod.console_set_default_background(0, libtcod.light_red)
        libtcod.console_set_default_foreground(0, libtcod.black)
        for x in range(60 +1):
            libtcod.console_print_ex(0, x, 1, libtcod.BKGND_SET, libtcod.CENTER, " ")
        libtcod.console_print_ex(0, 30, 1, libtcod.BKGND_SET, libtcod.CENTER, "You Died!")
        
        libtcod.console_set_default_foreground(0, libtcod.lighter_gray)
        libtcod.console_print_ex(0, 30, 2, libtcod.BKGND_NONE, libtcod.CENTER, "[ESC] to Close")

        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_print_ex(0, 30, 4, libtcod.BKGND_NONE, libtcod.CENTER, player.name + ", Level " + str(player.level.current_level))
        libtcod.console_print_ex(0, 30, 5, libtcod.BKGND_NONE, libtcod.CENTER, constants['options_difficulty'] + " " + constants['options_origin'])
        
        libtcod.console_set_default_foreground(0, screen_purple)
        libtcod.console_print_ex(0, 30, 6, libtcod.BKGND_NONE, libtcod.CENTER, str(player.turn_count) + " Turns")
        libtcod.console_print_ex(0, 30, 7, libtcod.BKGND_NONE, libtcod.CENTER, "Dungeon Level " + str(game_map.dungeon_level))
        libtcod.console_print_ex(0, 30, 7, libtcod.BKGND_NONE, libtcod.CENTER, str(player.score) + " Points")
        
        libtcod.console_set_default_foreground(0, screen_blue)
        libtcod.console_print_ex(0, 56, 6, libtcod.BKGND_NONE, libtcod.RIGHT, "Inventory")
        libtcod.console_set_default_foreground(0, libtcod.light_gray)
        i = 8
        for itm in player.inventory.items:
            msg = itm.name + ' ' + chr(itm.char)
            if itm.item.count > 1:
                msg = msg + " (x" + str(itm.item.count) + ")"
            libtcod.console_print_ex(0, 60 - 4, i, libtcod.BKGND_NONE, libtcod.RIGHT, msg)
            i = i + 1
        
        libtcod.console_set_default_foreground(0, screen_blue)
        libtcod.console_print_ex(0, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, "Kills")
        i = 8
        if len(player.kill_counts) == 0:
            libtcod.console_set_default_foreground(0, screen_yellow)
            libtcod.console_print_ex(0, 3, i, libtcod.BKGND_NONE, libtcod.LEFT, "No kills,")
            libtcod.console_print_ex(0, 5, i+1, libtcod.BKGND_NONE, libtcod.LEFT, "Pacifist mode!")
            
        else:
            libtcod.console_set_default_foreground(0, libtcod.lighter_gray)
            for pair in player.kill_counts:
                libtcod.console_print_ex(0, 3, i, libtcod.BKGND_NONE, libtcod.LEFT, chr(pair[2]) + ' ' + pair[0].title() + " x" + str(pair[1]))
                i = i + 1
         
        libtcod.console_flush()
        
        choice = key
        if choice.vk == libtcod.KEY_ESCAPE:
            return Message('You died!', libtcod.red), GameStates.PLAYER_DEAD
            break


def kill_monster(monster, player):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), libtcod.orange)
    
    found = False
    for kill in player.kill_counts:
        if found:
            break
            
        if kill[0] == monster.name:
            kill[1] = kill[1] + 1
            found = True
            
    if not found:
        player.kill_counts.append([monster.name, 1, monster.char])
        
    monster.char = 325
    monster.color = (255, 255, 177)
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    for con in monster.conditions: con.active = False

    return death_message
