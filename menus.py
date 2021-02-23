import tcod as libtcod
import textwrap
from game_messages import Message
from random_utils import left, mid, right

def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '[' + chr(letter_index) + '] ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2) + 16
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def game_options(constants):
 
    index = 0
 
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
       
    key = libtcod.Key()
    mouse = libtcod.Mouse()
     
    difficulty = "Newcomer"
            
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)

    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)
    
    for y in range(11, 29):
        for x in range(9, 49):
            libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
            if y == 28:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
            if x == 9 or x == 48:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT,chr(186))
                
    libtcod.console_print_ex(0, 9, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
    libtcod.console_print_ex(0, 26, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
           
    for x in range(9, 27):
        libtcod.console_print_ex(0, x, 9, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
        
    for x in range(26, 49):
        libtcod.console_print_ex(0, x, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
        
    #corners, T pieces
    libtcod.console_print_ex(0, 9, 9, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(0, 26, 9, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 9, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    libtcod.console_print_ex(0, 26, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 48, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(187))

    libtcod.console_print_ex(0, 9, 28, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 48, 28, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
           
    libtcod.console_set_default_foreground(0, screen_yellow)               
    libtcod.console_print_ex(0, 10, 10, libtcod.BKGND_SET, libtcod.LEFT, "New Game Options") 
    
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print_ex(0, 13, 26, libtcod.BKGND_SET, libtcod.LEFT, "Enter to accept, Esc to return") 
    libtcod.console_print_ex(0, 12, 27, libtcod.BKGND_SET, libtcod.LEFT, "Arrow keys to select/change options") 
    libtcod.console_set_default_foreground(0, libtcod.black)    
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        libtcod.console_set_default_foreground(0, screen_darkgray)
        libtcod.console_print_ex(0, 21, 12, libtcod.BKGND_SET, libtcod.LEFT, "              ")
        for y in range(11, 26):
            for x in range(10, 48):
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")

        libtcod.console_set_default_foreground(0, libtcod.black)
        strtut = "Disabled"
        if constants['options_tutorial_enabled']: strtut = "Enabled"
        
        libtcod.console_print_ex(0, 32, 14, libtcod.BKGND_SET, libtcod.RIGHT, "Tutorial Tips:")
        libtcod.console_print_ex(0, 34, 14, libtcod.BKGND_SET, libtcod.LEFT, strtut)
        
        libtcod.console_print_ex(0, 24, 12, libtcod.BKGND_SET, libtcod.LEFT, difficulty)
        
        if index == 0:
            libtcod.console_set_default_foreground(0, screen_green)
            libtcod.console_print_ex(0, 24, 12, libtcod.BKGND_SET, libtcod.LEFT, difficulty)
            
        if difficulty != "Newcomer":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 2, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(17))
            libtcod.console_print_ex(0, 22, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(17))
            
        if difficulty != " Custom ":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 33, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(16))
            libtcod.console_print_ex(0, 34, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(16))
            
        if difficulty == "Newcomer":
            desc = "Made for players less familiar with roguelike games. You do slightly more damage while enemies do slightly less. You also level up more quickly, and have slightly elevated luck."
        elif difficulty == "Classic":
            desc = "Typical roguelike style; Your enemies damage, your damage, experience and luck are all at their normal levels. No special help here, but no extra challenges either."
        elif difficulty == " Expert ":
            desc = "Choose this if you're looking for a bit of a challenge. Your enemies will be more hardy, and you will find yourself leveling at a slower pace. Your luck will be slightly lower as well."
        elif difficulty == " Sadist ":
            desc = "You do significantly less damage, enemies do more, XP trickles in at a sap-like pace, and your luck is that of someone who kicked a black cat through a mirror while standing under a ladder."
        elif difficulty == " Custom ":
            desc=""
            libtcod.console_set_default_foreground(0, libtcod.black)
            libtcod.console_print_ex(0, 32, 16, libtcod.BKGND_SET, libtcod.RIGHT, "Enemy Damage:") 
            libtcod.console_print_ex(0, 34, 16, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_enemy_damage_scale']) + "%")
            libtcod.console_print_ex(0, 32, 18, libtcod.BKGND_SET, libtcod.RIGHT, "Player Damage:")
            libtcod.console_print_ex(0, 34, 18, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_player_damage_scale']) + "%")
            libtcod.console_print_ex(0, 32, 20, libtcod.BKGND_SET, libtcod.RIGHT, "Experience Multiplier:") 
            libtcod.console_print_ex(0, 34, 20, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_xp_multiplier']) + "x")
            libtcod.console_print_ex(0, 32, 22, libtcod.BKGND_SET, libtcod.RIGHT, "Luck Scale:") 
            libtcod.console_print_ex(0, 34, 22, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_luck_scale']) + "%")
            #libtcod.console_print_ex(0, 32, 24, libtcod.BKGND_SET, libtcod.RIGHT, "Delete Save on Death:") 
            #strdel = "No"
            #if constants['options_death_delete_save']: strdel = "Yes"
            #libtcod.console_print_ex(0, 34, 24, libtcod.BKGND_SET, libtcod.LEFT, strdel)
        
        libtcod.console_set_default_foreground(0, screen_green)
        if index == 1:
            strtut = "Disabled"
            if constants['options_tutorial_enabled']: strtut = "Enabled"
            libtcod.console_print_ex(0, 32, 14, libtcod.BKGND_SET, libtcod.RIGHT, "Tutorial Tips:")
            libtcod.console_print_ex(0, 34, 14, libtcod.BKGND_SET, libtcod.LEFT, strtut)
            
        elif index == 2:
            libtcod.console_print_ex(0, 32, 16, libtcod.BKGND_SET, libtcod.RIGHT, "Enemy Damage:")
            libtcod.console_print_ex(0, 34, 16, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_enemy_damage_scale']) + "%")
            
        elif index == 3:
            libtcod.console_print_ex(0, 32, 18, libtcod.BKGND_SET, libtcod.RIGHT, "Player Damage:")
            libtcod.console_print_ex(0, 34, 18, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_player_damage_scale']) + "%")
            
        elif index == 4:
            libtcod.console_print_ex(0, 32, 20, libtcod.BKGND_SET, libtcod.RIGHT, "Experience Multiplier:")
            libtcod.console_print_ex(0, 34, 20, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_xp_multiplier']) + "x")
            
        elif index == 5:
            libtcod.console_print_ex(0, 32, 22, libtcod.BKGND_SET, libtcod.RIGHT, "Luck Scale:")
            libtcod.console_print_ex(0, 34, 22, libtcod.BKGND_SET, libtcod.LEFT, str(constants['options_luck_scale']) + "%")
            
            
        #elif index == 6:
        #    libtcod.console_print_ex(0, 32, 24, libtcod.BKGND_SET, libtcod.RIGHT, "Delete Save on Death:")
        #    strdel = "No"
        #    if constants['options_death_delete_save']: strdel = "Yes"
        #    libtcod.console_print_ex(0, 34, 24, libtcod.BKGND_SET, libtcod.LEFT, strdel)
            
        libtcod.console_set_default_foreground(0, screen_lightgray)

        description_lines = textwrap.wrap("  " + desc, 36)               #description for display in the inventory system
        y = 16
        for line in description_lines:
            libtcod.console_print_ex(0, 11, y, libtcod.BKGND_SET, libtcod.LEFT, line)
            y += 1
            
        libtcod.console_flush()

        if key.vk == libtcod.KEY_ENTER:            
        
            if difficulty == "Newcomer":
                constants['options_enemy_damage_scale'] = 80
                constants['options_player_damage_scale'] = 120
                constants['options_xp_multiplier'] = round(1.5, 1)
                constants['options_luck_scale'] = 150
                #constants['options_death_delete_save'] = False
                
            elif difficulty == "Classic":
                constants['options_enemy_damage_scale'] = 100
                constants['options_player_damage_scale'] = 100
                constants['options_xp_multiplier'] = 1
                constants['options_luck_scale'] = 100
                #constants['options_death_delete_save'] = True
                
            elif difficulty == " Expert ":
                constants['options_enemy_damage_scale'] = 130
                constants['options_player_damage_scale'] = 70
                constants['options_xp_multiplier'] = round(.5, 1)
                constants['options_luck_scale'] = 75
                #constants['options_death_delete_save'] = True
                
            elif difficulty == " Sadist ":
                constants['options_enemy_damage_scale'] = 200
                constants['options_player_damage_scale'] = 30
                constants['options_xp_multiplier'] = round(.1, 1)
                constants['options_luck_scale'] = 30
                #constants['options_death_delete_save'] = True
                
            constants['options_difficulty'] = difficulty.strip()
                
            break
            
        if key.vk == libtcod.KEY_ESCAPE:
            return "nah"
            
        elif key.vk == libtcod.KEY_RIGHT:
            if index == 0:
                if difficulty == "Newcomer":
                    difficulty = "Classic"
                elif difficulty == "Classic":
                    difficulty = " Expert "
                elif difficulty == " Expert ":
                    difficulty = " Sadist "
                elif difficulty == " Sadist ":
                    difficulty = " Custom "
            if index == 1: #tutorial tips
                constants['options_tutorial_enabled'] = not constants['options_tutorial_enabled']
            if index == 2:
                if constants['options_enemy_damage_scale'] < 990: constants['options_enemy_damage_scale'] += 10
            if index == 3:
                if constants['options_player_damage_scale'] < 990: constants['options_player_damage_scale'] += 10       
            if index == 4:
                if constants['options_xp_multiplier'] < 100:
                    if key.shift:
                        constants['options_xp_multiplier'] += 10
                    else:
                        constants['options_xp_multiplier'] = round(constants['options_xp_multiplier']+ 0.2, 1)
                    if constants['options_xp_multiplier'] > 100: constants['options_xp_multiplier'] = 100
            if index == 5:
                if constants['options_luck_scale'] < 990: constants['options_luck_scale'] += 10   
            #if index == 6:
                #constants['options_death_delete_save'] = not constants['options_death_delete_save']
                
        elif key.vk == libtcod.KEY_LEFT:
            if index == 0:  
                if difficulty == "Classic":
                    difficulty = "Newcomer"
                elif difficulty == " Expert ":
                    difficulty = "Classic"
                elif difficulty == " Sadist ":
                    difficulty = " Expert "
                elif difficulty == " Custom ":
                    difficulty = " Sadist "
            if index == 1:
                constants['options_tutorial_enabled'] = not constants['options_tutorial_enabled']
            if index == 2:
                if constants['options_enemy_damage_scale'] > 10: constants['options_enemy_damage_scale'] -= 10
            if index == 3:
                if constants['options_player_damage_scale'] > 10: constants['options_player_damage_scale'] -= 10    
            if index == 4:
                if constants['options_xp_multiplier'] > 0.2:
                    if key.shift:
                        constants['options_xp_multiplier'] = round(constants['options_xp_multiplier'] -10, 1)
                    else:
                        constants['options_xp_multiplier'] = round(constants['options_xp_multiplier'] - 0.2, 1)
                    if constants['options_xp_multiplier'] < 0.2: constants['options_xp_multiplier'] = 0.2
            if index == 5:
                if constants['options_luck_scale'] > 10: constants['options_luck_scale'] -= 10    
            #if index == 6:
            #    constants['options_death_delete_save'] = not constants['options_death_delete_save']         
               
        elif key.vk == libtcod.KEY_DOWN:
            if index == 0:
                index += 1
            elif index > 0:
                if difficulty == " Custom ":
                    if index < 5:
                        index += 1
            
        elif key.vk == libtcod.KEY_UP:
            if index > 0: index -= 1                
            
            
def origin_options(constants):
 
    index = 0
 
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
       
    key = libtcod.Key()
    mouse = libtcod.Mouse()
     
    origin = "Adventurer"
            
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)

    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)
    
    for y in range(11, 29):
        for x in range(9, 49):
            libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
            if y == 28:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
            if x == 9 or x == 48:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT,chr(186))
                
    libtcod.console_print_ex(0, 9, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
    libtcod.console_print_ex(0, 26, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
           
    for x in range(9, 27):
        libtcod.console_print_ex(0, x, 9, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
        
    for x in range(26, 49):
        libtcod.console_print_ex(0, x, 10, libtcod.BKGND_SET, libtcod.LEFT,chr(205))
        
    #corners, T pieces
    libtcod.console_print_ex(0, 9, 9, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(0, 26, 9, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 9, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
    libtcod.console_print_ex(0, 26, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 48, 10, libtcod.BKGND_SET, libtcod.LEFT, chr(187))

    libtcod.console_print_ex(0, 9, 28, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 48, 28, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
           
    libtcod.console_set_default_foreground(0, screen_yellow)               
    libtcod.console_print_ex(0, 10, 10, libtcod.BKGND_SET, libtcod.LEFT, "Character Origin") 
    
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print_ex(0, 13, 26, libtcod.BKGND_SET, libtcod.LEFT, "Enter to accept, Esc to return") 
    libtcod.console_print_ex(0, 14, 27, libtcod.BKGND_SET, libtcod.LEFT, "Left/Right to change options") 
    libtcod.console_set_default_foreground(0, libtcod.black)    
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        libtcod.console_set_default_foreground(0, screen_darkgray)
        libtcod.console_print_ex(0, 21, 12, libtcod.BKGND_SET, libtcod.LEFT, "              ")
        for y in range(11, 26):
            for x in range(10, 48):
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")

        libtcod.console_set_default_foreground(0, screen_blue)       
        libtcod.console_print_ex(0, 11, 20, libtcod.BKGND_SET, libtcod.LEFT, "Starting Equipment;")

        
        libtcod.console_print_ex(0, 24, 12, libtcod.BKGND_SET, libtcod.LEFT, origin)
        
        if index == 0:
            libtcod.console_set_default_foreground(0, screen_green)
            libtcod.console_print_ex(0, 24, 12, libtcod.BKGND_SET, libtcod.LEFT, origin)
            
        if origin != "Adventurer":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 21, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(17))
            libtcod.console_print_ex(0, 22, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(17))
            
        if origin != "Tourist":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 33, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(16))
            libtcod.console_print_ex(0, 34, 12, libtcod.BKGND_SET, libtcod.LEFT, chr(16))
            
        libtcod.console_set_default_foreground(0, screen_lightgray)  
        if origin == "Adventurer":
            desc = "A classic sword-and-shield adventurer, you are more suited to the challenge of the wizards' dungeon than most. We'll see how much of a difference that makes."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(369) + " Sword (+3 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(375) + " Shield (+1 DEF)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 10 Gold")
             
        elif origin == "Merchant":
            desc = "Though not the typical fighting type yourself, you've seen your share of scuffs and challenges. Your ability to swindle and swoon may come in handy."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(372) + " Staff (+2 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(364) + " Merchants Bag (+24 Carrying)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 100 Gold")
            
        elif origin == "Criminal":
            desc = "Bad boi"
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(368) + " Dagger (+2 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(382) + " Fingerless Gloves (+3 SPD)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 30 Gold")
            
        elif origin == "Tourist": 
            desc= "This is why they say not to travel, just to stay at home. You were only wanting to get some time away from home, and now you're someone elses warning story."
        
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(395) + " Cargo Shorts (+8 Carrying)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 10 Gold")

        constants['options_origin'] = origin
        
        libtcod.console_set_default_foreground(0, screen_green)
        if index == 0:
            libtcod.console_print_ex(0, 24, 12, libtcod.BKGND_SET, libtcod.LEFT, origin)
            
      
            
        libtcod.console_set_default_foreground(0, screen_lightgray)

        description_lines = textwrap.wrap("  " + desc, 36)               #description for display in the inventory system
        y = 14
        for line in description_lines:
            libtcod.console_print_ex(0, 11, y, libtcod.BKGND_SET, libtcod.LEFT, line)
            y += 1
            
        libtcod.console_flush()

        if key.vk == libtcod.KEY_ENTER:            
        
            if origin == "Adventurer":
                x=1
                
            elif origin == "Merchant":
                x=1
                
            elif origin == "Criminal":
                x=1
                
            elif origin == "Tourist":
                x=1
            
            break
            
        if key.vk == libtcod.KEY_ESCAPE:
            return "nah"
            
        elif key.vk == libtcod.KEY_RIGHT:
            if index == 0:
                if origin == "Adventurer":
                    origin = "Merchant"
                    
                elif origin == "Merchant":
                    origin = "Criminal"
                    
                elif origin == "Criminal":
                    origin = "Tourist"
      
        elif key.vk == libtcod.KEY_LEFT:
            if index == 0:  
                if origin == "Merchant":
                    origin = "Adventurer"
                    
                elif origin == "Criminal":
                    origin = "Merchant"
                    
                elif origin == "Tourist":
                    origin = "Criminal"
            

def inventory_menu(player, entities, fov_map, names_list, colors_list):
    
    results = []
    
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
    
    index = 0
    
    itemsperpage = 24
    numitems = len(player.inventory.items)
    
    if numitems == 0:
        results.append({'message': Message("Ya' cabbash", libtcod.white)})
        return results
    
    numpages = int(numitems / itemsperpage) + 1
    currentpage = 1
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
     
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)
    
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)
    
    #backgrounds and border
    for y in range (2, 39):
        for x in range (1, 59):
            libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
            if y == 2 or y == 11 or y == 38:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
   
    for x in range(1, 12):
        libtcod.console_print_ex(0, x, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        
    for y in range(2, 39):
        libtcod.console_print_ex(0, 1, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        libtcod.console_print_ex(0, 58, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        
    #corners, T pieces
    libtcod.console_print_ex(0, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(0, 11, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 11, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 58, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 1, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(199))
    libtcod.console_print_ex(0, 58, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(182))
    libtcod.console_print_ex(0, 1, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 58, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
  
    #stats, slots
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, screen_blue)
    
    libtcod.console_print_ex(0, 9, 5, libtcod.BKGND_SET, libtcod.RIGHT, "Attack")
    libtcod.console_print_ex(0, 9, 7, libtcod.BKGND_SET, libtcod.RIGHT, "Defense")
    libtcod.console_print_ex(0, 9, 9, libtcod.BKGND_SET, libtcod.RIGHT, "Speed")
    
    libtcod.console_print_ex(0, 24, 5, libtcod.BKGND_SET, libtcod.RIGHT, "Main Hand")
    libtcod.console_print_ex(0, 24, 7, libtcod.BKGND_SET, libtcod.RIGHT, "Off Hand")
    libtcod.console_print_ex(0, 24, 9, libtcod.BKGND_SET, libtcod.RIGHT, "Accessory")
    
    libtcod.console_print_ex(0, 45, 5, libtcod.BKGND_SET, libtcod.RIGHT, "Helm")
    libtcod.console_print_ex(0, 45, 7, libtcod.BKGND_SET, libtcod.RIGHT, "Armor")
    libtcod.console_print_ex(0, 45, 9, libtcod.BKGND_SET, libtcod.RIGHT, "Accessory")
    
    libtcod.console_set_default_foreground(0, screen_yellow)
    libtcod.console_print_ex(0, 2, 2, libtcod.BKGND_SET, libtcod.LEFT, "Inventory")
    
    libtcod.console_set_default_foreground(0, screen_lightgray)
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "[Escape to Close]")
    
    while True:
    
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_set_default_background(0, screen_darkgray)
        
        libtcod.console_print_ex(0, 31, 32, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to use or equip")
        
        libtcod.console_print_ex(0, 31, 34, libtcod.BKGND_SET, libtcod.LEFT, "[A]pply [D]rop [T]hrow")
        
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, chr(30)) #up
        libtcod.console_print_ex(0, 32, 36, libtcod.BKGND_SET, libtcod.LEFT, chr(31)) #down
        
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, "                      ")
        libtcod.console_set_default_foreground(0, screen_midgray)
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, "Page " + str(currentpage) + " of " + str(numpages))
        libtcod.console_print_ex(0, 44, 36, libtcod.BKGND_SET, libtcod.LEFT, "Cap. " + str(numitems) + " of " + str(player.inventory.max_capacity))
        
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        #inventory space
        for y in range(13, 13+itemsperpage):
            for x in range(3, 30):
                if y % 2 == 0: #even
                    libtcod.console_set_default_background(0, screen_midgray)
                else: #odd
                    libtcod.console_set_default_background(0, screen_lightgray)
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
                
        libtcod.console_set_default_foreground(0, libtcod.black)
        y = 13
        start = (currentpage - 1) * itemsperpage
        for x in range(start, start + itemsperpage):
            if x < numitems:
                item = player.inventory.items[x] 
                istr = chr(item.char) + " " + names_list[item.name]
                for e in player.equipment.list:
                    if e and names_list[item.name] == e.name:
                        istr = "> " + istr
                if len(istr) + 5 > 25: istr = left(istr,25) #ensure that the item, + '(x00)' is less than 25 characters wide
                if item.item.stackable and item.item.count > 1: istr = istr + " (x" + str(item.item.count) + ")"
                libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, istr)
                y += 1
        
        #player stats
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_print_ex(0, 11, 5, libtcod.BKGND_SET, libtcod.LEFT, str(player.fighter.power))
        libtcod.console_print_ex(0, 11, 7, libtcod.BKGND_SET, libtcod.LEFT, str(player.fighter.defense))
        libtcod.console_print_ex(0, 11, 9, libtcod.BKGND_SET, libtcod.LEFT, str(player.fighter.speed))

        libtcod.console_print_ex(0, 26, 5, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        libtcod.console_print_ex(0, 26, 6, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        libtcod.console_print_ex(0, 26, 7, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        libtcod.console_print_ex(0, 47, 5, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        libtcod.console_print_ex(0, 47, 6, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        libtcod.console_print_ex(0, 47, 7, libtcod.BKGND_SET, libtcod.LEFT, "          ")
        #equipment
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.main_hand: 
            libtcod.console_set_default_foreground(0, screen_yellow)
            ename = player.equipment.main_hand.name
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 26, 5, libtcod.BKGND_SET, libtcod.LEFT, ename)
        
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.off_hand:
            ename = player.equipment.off_hand.name
            libtcod.console_set_default_foreground(0, screen_yellow)
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 26, 7, libtcod.BKGND_SET, libtcod.LEFT, ename)
        
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.accessory1:
            ename = player.equipment.accessory1.name
            libtcod.console_set_default_foreground(0, screen_yellow)
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 26, 9, libtcod.BKGND_SET, libtcod.LEFT, ename)
        
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.helm:
            ename = player.equipment.helm.name
            libtcod.console_set_default_foreground(0, screen_yellow)
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 47, 5, libtcod.BKGND_SET, libtcod.LEFT, ename)
        
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.armor:
            libtcod.console_set_default_foreground(0, screen_yellow)
            ename = player.equipment.armor.name
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 47, 7, libtcod.BKGND_SET, libtcod.LEFT, ename)
        
        ename = "[  None  ]"
        libtcod.console_set_default_foreground(0, screen_midgray)
        if player.equipment.accessory2:
            ename = player.equipment.accessory2.name
            libtcod.console_set_default_foreground(0, screen_yellow)
        if len(ename) > 10: ename = left(ename,10)
        libtcod.console_print_ex(0, 47, 9, libtcod.BKGND_SET, libtcod.LEFT, ename)
            
        libtcod.console_set_default_background(0, screen_green)
        libtcod.console_set_default_foreground(0, screen_red)
        
        #update index based on mouse position
        if (mouse.cx >2 and mouse.cx < 30) and (mouse.cy > 12 and mouse.cy < 37):
            selectedline = mouse.cy - 12
            index = (((currentpage-1)*itemsperpage) + (selectedline-1))
            if index > numitems - 1: index = numitems - 1

        #green selection line
        line = 13 + (index%itemsperpage)
        item = player.inventory.items[index]
        
        stritem = chr(item.char) + " " + names_list[item.name]
        if item.item.stackable and item.item.count > 1: stritem = stritem + " (x" + str(item.item.count) + ")"
        
        for e in player.equipment.list:
                    if e and names_list[item.name] == e.name:
                        stritem = "> " + stritem
        
        for i in range (27 - len(stritem)):
            stritem = stritem + " "
        
        if currentpage > 1: libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, chr(30)) #up
        if currentpage < numpages: libtcod.console_print_ex(0, 32, 36, libtcod.BKGND_SET, libtcod.LEFT, chr(31)) #down)
        
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_SET, libtcod.LEFT, stritem)
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        for y in range (15, 26+1):
            libtcod.console_print_ex(0, 44, y, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        for y in range (28, 30+1):
            libtcod.console_print_ex(0, 44, y, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        libtcod.console_set_default_background(0, screen_midgray)
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, " " + chr(item.char) + " " + names_list[item.name] + " ")
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)

        lines = item.item.description_lines
        
        y = 15
        for l in lines:
            libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
            y+=1           
            
        if item.item.effect_lines: # TODO :: Build in check for unidentified items 
            y += 1 #start the effect text after the description text ends.
            for l in item.item.effect_lines:
                libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
                y+=1    
        
        if item.equippable:
            
            libtcod.console_set_default_background(0, screen_darkgray)
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 32, 28, libtcod.BKGND_NONE, libtcod.LEFT, "ATK.")
            libtcod.console_print_ex(0, 32, 29, libtcod.BKGND_NONE, libtcod.LEFT, "DEF.")
            libtcod.console_print_ex(0, 32, 30, libtcod.BKGND_NONE, libtcod.LEFT, "SPD.")
            
            libtcod.console_print_ex(0, 41, 28, libtcod.BKGND_NONE, libtcod.LEFT, "MHP.")
            libtcod.console_print_ex(0, 41, 29, libtcod.BKGND_NONE, libtcod.LEFT, "LCK.")
            libtcod.console_print_ex(0, 41, 30, libtcod.BKGND_NONE, libtcod.LEFT, "****")
            
            libtcod.console_print_ex(0, 50, 28, libtcod.BKGND_NONE, libtcod.LEFT, "****")
            libtcod.console_print_ex(0, 50, 29, libtcod.BKGND_NONE, libtcod.LEFT, "****")
            libtcod.console_print_ex(0, 50, 30, libtcod.BKGND_NONE, libtcod.LEFT, "****")
            
            libtcod.console_set_default_foreground(0, screen_midgray)
            libtcod.console_print_ex(0, 37, 28, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 37, 29, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 37, 30, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 46, 28, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 46, 29, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 46, 30, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 55, 28, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 55, 29, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            libtcod.console_print_ex(0, 55, 30, libtcod.BKGND_NONE, libtcod.LEFT, "00")
            
            ## THIS WHOLE SECTION IS DISPLAYING STATS INCORECTLY ..
                # NEED TO CHECK IF ALREADY EQUIPPED OR NOT
                # NEED TO CHECK CURRENT POWER +/- THIS POWER BONUS, NOT JUST BASE

            if item.equippable.power_bonus > 0:
                libtcod.console_set_default_foreground(0, screen_green)
                strpower = str(item.equippable.power_bonus)
                strpower = str((player.fighter.base_power + item.equippable.power_bonus) - player.fighter.power)
                if int(strpower) < 0:
                    libtcod.console_set_default_foreground(0, screen_red)
                elif int(strpower) == 0:
                    libtcod.console_set_default_foreground(0, screen_midgray)
                if len(strpower) < 2: strpower = "0" + strpower
                libtcod.console_print_ex(0, 37, 28, libtcod.BKGND_NONE, libtcod.LEFT, strpower)
            
            if item.equippable.defense_bonus > 0:
                libtcod.console_set_default_foreground(0, screen_green)
                strdef = str((player.fighter.base_defense + item.equippable.defense_bonus) - player.fighter.defense)
                if int(strdef) < 0:
                    libtcod.console_set_default_foreground(0, screen_red)
                elif int(strdef) == 0:
                    libtcod.console_set_default_foreground(0, screen_midgray)
                if len(strdef) < 2: strdef = "0" + strdef  
                libtcod.console_print_ex(0, 37, 29, libtcod.BKGND_NONE, libtcod.LEFT, strdef)
            
            if item.equippable.speed_bonus > 0:
                libtcod.console_set_default_foreground(0, screen_green)
                strspeed = str((player.fighter.base_speed + item.equippable.speed_bonus) - player.fighter.speed)
                if int(strspeed) < 0:
                    libtcod.console_set_default_foreground(0, screen_red)
                elif int(strspeed) == 0:
                    libtcod.console_set_default_foreground(0, screen_midgray)
                if len(strspeed) < 2: strspeed = "0" + strspeed
                libtcod.console_print_ex(0, 37, 30, libtcod.BKGND_NONE, libtcod.LEFT, strspeed)
            
            if item.equippable.max_hp_bonus > 0:
                libtcod.console_set_default_foreground(0, screen_green)
                strmhp = str((player.fighter.base_max_hp + item.equippable.max_hp_bonus) - player.fighter.max_hp)
                if int(strmhp) < 0:
                    libtcod.console_set_default_foreground(0, screen_red)
                elif int(strmhp) == 0:
                    libtcod.console_set_default_foreground(0, screen_midgray)
                if len(strmhp) < 2: strmhp = "0" + strmhp
                libtcod.console_print_ex(0, 46, 28, libtcod.BKGND_NONE, libtcod.LEFT, strmhp)
                
            if item.equippable.luck_bonus > 0:
                libtcod.console_set_default_foreground(0, screen_green)    
                strlck = str((player.fighter.base_luck + item.equippable.luck_bonus) - player.fighter.luck)
                if int(strlck) < 0: 
                    libtcod.console_set_default_foreground(0, screen_red)
                elif int(strlck) == 0:
                    libtcod.console_set_default_foreground(0, screen_midgray)
                if len(strlck) < 2: strlck = "0" + strlck            
                libtcod.console_print_ex(0, 46, 29, libtcod.BKGND_NONE, libtcod.LEFT, strlck)
            
        libtcod.console_set_default_foreground(0, libtcod.white)
        if item.item.use_function or item.equippable: 
            libtcod.console_print_ex(0, 31, 32, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to use or equip")
        
        libtcod.console_print_ex(0, 31, 34, libtcod.BKGND_SET, libtcod.LEFT, "[A]pply [D]rop [T]hrow")
        libtcod.console_set_default_foreground(0, screen_yellow)
        
        libtcod.console_print_ex(0, 40, 34, libtcod.BKGND_NONE, libtcod.LEFT, "D")
        libtcod.console_set_default_foreground(0, screen_red)
        
        libtcod.console_print_ex(0, 32, 34, libtcod.BKGND_NONE, libtcod.LEFT, "A")
        libtcod.console_print_ex(0, 47, 34, libtcod.BKGND_NONE, libtcod.LEFT, "T")
            
        libtcod.console_flush()

        m = libtcod.mouse_get_status()
        click = m.lbutton_pressed

        if click:
            if (mouse.cx >2 and mouse.cx < 30) and (mouse.cy > 12 and mouse.cy < 37):
                if item.item.use_function:
                    results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list))
                    item.identified = True
                    return results
                elif item.equippable:
                    player.equipment.toggle_equip(item)
            elif mouse.cx == 31 and mouse.cy == 36 and currentpage > 1:
                currentpage -= 1
                index = (itemsperpage * currentpage) - 1
            elif mouse.cx == 32 and mouse.cy == 36 and currentpage <  numpages:
                currentpage += 1
                index = (currentpage -1) * itemsperpage
                if index >  numitems -1 : index = numitems - 1
                
        if key.vk == libtcod.KEY_ESCAPE or chr(key.c) == "i":
            #results.append({'ignore': 0})
            return results
   
        elif key.vk == libtcod.KEY_DOWN:
            if index < numitems-1: index += 1
            if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        elif key.vk == libtcod.KEY_UP:
            if index > 0: index -= 1
            if line == 13 and currentpage > 1: currentpage -= 1
            
        elif key.vk == libtcod.KEY_ENTER:
            if item.item.use_function:
                results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list, colors_list=colors_list))
                return results
                
            elif item.equippable:
                player.equipment.toggle_equip(item)
    
        elif chr(key.c) == "d":
            results.extend(player.inventory.drop_item(item))
            return results


def old_inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append('{0} (on main hand)'.format(names_list[item.name]))
            elif player.equipment.off_hand == item:
                options.append('{0} (on off hand)'.format(names_list[item.name]))
            else:
                strlist = names_list[item.name]
                if item.item.stackable and item.item.count >1:
                    strlist = strlist + " (x" + str(item.item.count) + ")"
                    
                options.append(strlist)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):

    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.black)
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'LIGHTS,')
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'CAMERA,')
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'ACTION!')


    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height-20)


def old_character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 2, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Level: {0}'.format(player.level.current_level))
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience: {0}'.format(player.level.current_xp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Experience to Level: {0}'.format(player.level.experience_to_next_level))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 8, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defense: {0}'.format(player.fighter.defense))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)

def character_screen(player, entities, constants, dungeon_level, names_list, colors_list):
    
    results = []
    
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
    
    index = 0
    
    itemsperpage = 24
    numitems = len(player.inventory.items)
    
    if numitems == 0:
        results.append({'message': Message("Ya' cabbash", libtcod.white)})
        return results
    
    numpages = int(numitems / itemsperpage) + 1
    currentpage = 1
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
     
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_clear(0)
    
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)
    
    #backgrounds and border
    for y in range (2, 39):
        for x in range (1, 59):
            libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
            if y == 2 or y == 38:
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
   
    for x in range(1, 12):
        libtcod.console_print_ex(0, x, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
        
    for y in range(2, 39):
        libtcod.console_print_ex(0, 1, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        libtcod.console_print_ex(0, 58, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        
    #corners, T pieces
    libtcod.console_print_ex(0, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    libtcod.console_print_ex(0, 11, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 11, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 58, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    libtcod.console_print_ex(0, 1, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    libtcod.console_print_ex(0, 58, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
  
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, screen_yellow)           
    libtcod.console_print_ex(0, 2, 2, libtcod.BKGND_SET, libtcod.LEFT, "Character")
    
    libtcod.console_set_default_foreground(0, screen_lightgray)

    libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "[Escape to Close]")
    
    libtcod.console_set_default_foreground(0, screen_yellow)
    libtcod.console_print_ex(0, 3, 5, libtcod.BKGND_NONE, libtcod.LEFT, player.name + ", Level " + str(player.level.current_level))
    libtcod.console_print_ex(0, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, constants['options_difficulty'] + " " + constants['options_origin'])
    
    libtcod.console_set_default_foreground(0, screen_purple)
    libtcod.console_print_ex(0, 3, 8, libtcod.BKGND_NONE, libtcod.LEFT, str(player.turn_count) + " Turns")
    libtcod.console_print_ex(0, 3, 9, libtcod.BKGND_NONE, libtcod.LEFT, "Dungeon Level " + str(dungeon_level))
        
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        libtcod.console_flush()
                
        if key.vk == libtcod.KEY_ESCAPE or chr(key.c) == "s":
            #results.append({'ignore': 0})
            return results

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)
