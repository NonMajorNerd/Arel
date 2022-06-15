from numpy import SHIFT_DIVIDEBYZERO
import tcod as libtcod
import textwrap
import operator
from game_messages import Message
from loader_functions.data_loaders import load_high_scores
from random_utils import left, mid, right, myattrgetter
from equipment_slots import EquipmentSlots

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

def intro(constants):

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
    
    step = 1
    
    libtcod.console_set_default_background(0, libtcod.black)
    libtcod.console_set_default_foreground(0, screen_lightgray)
    libtcod.console_clear(0)
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_clear(0)

        if step == 1:
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            
        elif step == 2:
            libtcod.console_print_ex(0, 30, 19, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
        elif step == 3:
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 18, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            
        elif step == 4:
            libtcod.console_print_ex(0, 30, 16, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 19, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            
        elif step == 5:
            libtcod.console_print_ex(0, 30, 15, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 16, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 18, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 19, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
        
        elif step == 6:
            libtcod.console_print_ex(0, 30, 13, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 14, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 16, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 18, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
            
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "That's right, I am Viodum the Adept!")
            
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 31, 20, libtcod.BKGND_SET, libtcod.LEFT, "Viodum the Adept")
            
        elif step == 7:
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 13, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 15, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 16, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
            
            libtcod.console_print_ex(0, 30, 19, libtcod.BKGND_SET, libtcod.CENTER, "That's right, I am Viodum the Adept!")
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "And you're on Vidoum's Victims!")
            
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 31, 19, libtcod.BKGND_SET, libtcod.LEFT, "Viodum the Adept")
            libtcod.console_set_default_foreground(0, screen_red)
            libtcod.console_print_ex(0, 29, 20, libtcod.BKGND_SET, libtcod.LEFT, "Viodum's Victims")
            
        elif step == 8:
            libtcod.console_print_ex(0, 30, 10, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 11, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 13, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 14, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 15, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
            
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "That's right, I am Viodum the Adept!")
            libtcod.console_print_ex(0, 30, 18, libtcod.BKGND_SET, libtcod.CENTER, "And you're on Vidoum's Victims!")
            
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "WAIT, I MEANT VICTORS! VIODUM'S VICTORS!")
            
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 31, 17, libtcod.BKGND_SET, libtcod.LEFT, "Viodum the Adept")
            libtcod.console_set_default_foreground(0, screen_red)
            libtcod.console_print_ex(0, 29, 18, libtcod.BKGND_SET, libtcod.LEFT, "Viodum's Victims")
            
            libtcod.console_print_ex(0, 33, 20, libtcod.BKGND_SET, libtcod.LEFT, "VIODUM'S VICTORS")
            libtcod.console_set_default_foreground(0, screen_yellow)
            libtcod.console_print_ex(0, 24, 20, libtcod.BKGND_SET, libtcod.LEFT, "VICTORS")
            
        elif step == 9:
            libtcod.console_print_ex(0, 30, 9, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 10, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 11, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 13, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
            
            libtcod.console_print_ex(0, 30, 15, libtcod.BKGND_SET, libtcod.CENTER, "That's right, I am Viodum the Adept!")
            libtcod.console_print_ex(0, 30, 16, libtcod.BKGND_SET, libtcod.CENTER, "And you're on Vidoum's Victims!")
            
            libtcod.console_print_ex(0, 30, 18, libtcod.BKGND_SET, libtcod.CENTER, "WAIT, I MEANT VICTORS! VIODUM'S VICTORS!")
            
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "Don't be scared..")
            
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 31, 15, libtcod.BKGND_SET, libtcod.LEFT, "Viodum the Adept")
            libtcod.console_set_default_foreground(0, screen_red)
            libtcod.console_print_ex(0, 29, 16, libtcod.BKGND_SET, libtcod.LEFT, "Viodum's Victims")
            
            libtcod.console_print_ex(0, 33, 18, libtcod.BKGND_SET, libtcod.LEFT, "VIODUM'S VICTORS")
            libtcod.console_set_default_foreground(0, screen_yellow)
            libtcod.console_print_ex(0, 24, 18, libtcod.BKGND_SET, libtcod.LEFT, "VICTORS")
            
        elif step == 10:
            libtcod.console_print_ex(0, 30, 8, libtcod.BKGND_SET, libtcod.CENTER, "Awake, weary traveler.. ")
            libtcod.console_print_ex(0, 30, 9, libtcod.BKGND_SET, libtcod.CENTER, "You've been asleep for some time, now.")
            
            libtcod.console_print_ex(0, 30, 10, libtcod.BKGND_SET, libtcod.CENTER, "Sorry to have interrupted your plans..")
            libtcod.console_print_ex(0, 30, 11, libtcod.BKGND_SET, libtcod.CENTER, "But you should be excited..")
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, "You're my latest contenstant!")
            
            libtcod.console_print_ex(0, 30, 14, libtcod.BKGND_SET, libtcod.CENTER, "That's right, I am Viodum the Adept!")
            libtcod.console_print_ex(0, 30, 15, libtcod.BKGND_SET, libtcod.CENTER, "And you're on Vidoum's Victims!")
            
            libtcod.console_print_ex(0, 30, 17, libtcod.BKGND_SET, libtcod.CENTER, "WAIT, I MEANT VICTORS! VIODUM'S VICTORS!")
            
            libtcod.console_print_ex(0, 30, 19, libtcod.BKGND_SET, libtcod.CENTER, "Don't be scared..")
            
            libtcod.console_set_default_foreground(0, screen_blue)
            libtcod.console_print_ex(0, 31, 14, libtcod.BKGND_SET, libtcod.LEFT, "Viodum the Adept")
            libtcod.console_set_default_foreground(0, screen_red)
            libtcod.console_print_ex(0, 29, 15, libtcod.BKGND_SET, libtcod.LEFT, "Viodum's Victims")
            
            libtcod.console_print_ex(0, 33, 17, libtcod.BKGND_SET, libtcod.LEFT, "VIODUM'S VICTORS")
            libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, "You're going to do great.")
            libtcod.console_set_default_foreground(0, screen_yellow)
            libtcod.console_print_ex(0, 24, 17, libtcod.BKGND_SET, libtcod.LEFT, "VICTORS")
            
        libtcod.console_set_default_foreground(0, screen_midgray)
        libtcod.console_print_ex(0, 30, 38, libtcod.BKGND_SET, libtcod.CENTER, "[Enter] to continue, [Esc] to skip")
        
        libtcod.console_flush()
        
        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:
            if step == 10:
                return True
            else:
                step += 1
                
        if key.vk == libtcod.KEY_ESCAPE:          
            return True

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
     
    difficulty = "Classic"
            
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
        
        libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, difficulty)
        
        if index == 0:
            libtcod.console_set_default_foreground(0, screen_green)
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, difficulty)
            
        if difficulty != "Newcomer":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 22, 12, libtcod.BKGND_SET, libtcod.LEFT, "<<")

            
        if difficulty != "Custom":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 36, 12, libtcod.BKGND_SET, libtcod.LEFT, ">>")
            
        if difficulty == "Newcomer":
            desc = "Made for players less familiar with roguelike games. You do slightly more damage while enemies do slightly less. You also level up more quickly, and have slightly elevated luck."
        elif difficulty == "Classic":
            desc = "Typical roguelike style; Your enemies damage, your damage, experience and luck are all at their normal levels. No special help here, but no extra challenges either."
        elif difficulty == "Expert":
            desc = "Choose this if you're looking for a bit of a challenge. Your enemies will be more hardy, and you will find yourself leveling at a slower pace. Your luck will be slightly lower as well."
        elif difficulty == "Sadist":
            desc = "You do significantly less damage, enemies do more, XP trickles in at a sap-like pace, and your luck is that of someone who kicked a black cat through a mirror while standing under a ladder."
        elif difficulty == "Custom":
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

        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:            
        
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
                
            elif difficulty == "Expert":
                constants['options_enemy_damage_scale'] = 130
                constants['options_player_damage_scale'] = 70
                constants['options_xp_multiplier'] = round(.5, 1)
                constants['options_luck_scale'] = 75
                #constants['options_death_delete_save'] = True
                
            elif difficulty == "Sadist":
                constants['options_enemy_damage_scale'] = 200
                constants['options_player_damage_scale'] = 30
                constants['options_xp_multiplier'] = round(.1, 1)
                constants['options_luck_scale'] = 30
                #constants['options_death_delete_save'] = True
                
            constants['options_difficulty'] = difficulty
                
            break
            
        if key.vk == libtcod.KEY_ESCAPE:
            return "nah"
            
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            if index == 0:
                if difficulty == "Newcomer":
                    difficulty = "Classic"
                elif difficulty == "Classic":
                    difficulty = "Expert"
                elif difficulty == "Expert":
                    difficulty = "Sadist"
                elif difficulty == "Sadist":
                    difficulty = "Custom"
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
                
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            if index == 0:  
                if difficulty == "Classic":
                    difficulty = "Newcomer"
                elif difficulty == "Expert":
                    difficulty = "Classic"
                elif difficulty == "Sadist":
                    difficulty = "Expert"
                elif difficulty == "Custom":
                    difficulty = "Sadist"
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
               
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            if index == 0:
                index += 1
            elif index > 0:
                if difficulty == "Custom":
                    if index < 5:
                        index += 1
            
        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            if index > 0: index -= 1                
            

def m1m2_menu(x=1, y=1, w=None, h=None, numoptions=3, optionslist=[]):

    if optionslist == []: return False
   
    results = None
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    inv_index = 0
    m1_index = 0

    if h == numoptions: h += 3
    if w < 18: w = 18
    #print static UI elements
    if True:
        libtcod.console_set_default_foreground(0, libtcod.black)
        libtcod.console_set_default_background(0, screen_darkgray)

        for ix in range (x, x+w+1):
            for iy in range(y, y+h+1):
                libtcod.console_print_ex(0, ix, iy, libtcod.BKGND_SET, libtcod.LEFT, " ")

        #corners, T pieces
        libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, chr(201))     # Top Left Corner  |'
        libtcod.console_print_ex(0, x+w, y, libtcod.BKGND_SET, libtcod.LEFT, chr(187))   # Top Right Corner `|
        libtcod.console_print_ex(0, x, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(200))   # Bottom Left Corner |_
        libtcod.console_print_ex(0, x+w, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(188)) # Bottom Right Corner _|       

        for ix in range(x+1, x+w):
            libtcod.console_print_ex(0, ix, y, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
            libtcod.console_print_ex(0, ix, y+h, libtcod.BKGND_SET, libtcod.LEFT, chr(205))

        for iy in range(y+1, y+h):
            libtcod.console_print_ex(0, x, iy, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
            libtcod.console_print_ex(0, x+w, iy, libtcod.BKGND_SET, libtcod.LEFT, chr(186))


        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_print_ex(0, int(x+(w/2)), y+h-2, libtcod.BKGND_NONE, libtcod.CENTER, "[Enter] to Select")
        libtcod.console_print_ex(0, int(x+(w/2)), y+h-1, libtcod.BKGND_NONE, libtcod.CENTER, "[Esc] to Cancel")

        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_print_ex(0, int(x+(w/2)), y, libtcod.BKGND_NONE, libtcod.CENTER, "Firing Preference")

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    libtcod.console_set_default_foreground(0, libtcod.black)

    while True:
        for iy in range (1, numoptions+1):
            for ix in range (x+1, x+w):
                if iy %2 == 0:
                    libtcod.console_set_default_background(0, screen_midgray)
                    libtcod.console_print_ex(0, ix, y+iy, libtcod.BKGND_SET, libtcod.LEFT, " ")
                else:
                    libtcod.console_set_default_background(0, screen_lightgray)
                    libtcod.console_print_ex(0, ix, y+iy, libtcod.BKGND_SET, libtcod.LEFT, " ")

        if len(optionslist) < numoptions:
            for opt in optionslist: 
                libtcod.console_print_ex(0, x+1, y+1+optionslist.index(opt), libtcod.BKGND_NONE, libtcod.LEFT, str(opt))
        else:
            for i in range (0, numoptions):     
                libtcod.console_print_ex(0, x+1, y+1+i, libtcod.BKGND_NONE, libtcod.LEFT, str(optionslist[inv_index + i]))

        current_option = optionslist[inv_index + m1_index]
        libtcod.console_set_default_background(0, screen_green)

        for iw in range(x+1, x+(w-len(current_option))):
            current_option = current_option + " "

        libtcod.console_print_ex(0, x+1, y+1+m1_index, libtcod.BKGND_SET, libtcod.LEFT, current_option)

        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        if key.vk == libtcod.KEY_ESCAPE:
            return('exit')

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            if m1_index == 0:
                if inv_index > 0:
                    inv_index -= 1

            else:
                m1_index -= 1

        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            if m1_index < len(optionslist) -1:
                if m1_index == numoptions-1:
                    if inv_index < len(optionslist)-numoptions:
                        inv_index += 1
                    
                else:
                    m1_index += 1

        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:
            return current_option.strip()

            
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

        
        libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, origin)
        
        if index == 0:
            libtcod.console_set_default_foreground(0, screen_green)
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, origin)
            
        if origin != "Adventurer":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 22, 12, libtcod.BKGND_SET, libtcod.LEFT, "<<")
            
        if origin != "Tourist":
            libtcod.console_set_default_foreground(0, screen_yellow)               
            libtcod.console_print_ex(0, 36, 12, libtcod.BKGND_SET, libtcod.LEFT, ">>")
            

        libtcod.console_set_default_foreground(0, screen_lightgray)  

        if origin == "Adventurer":
            
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(258))
            
            desc = "A classic sword-and-shield adventurer, you are more suited to the challenge my dungeon than most. We'll see how much of a difference that makes."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(369) + " Sword (+3 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(375) + " Shield (+1 DEF)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 20 Gold")

        elif origin == "Ranger":
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(257))
            
            desc = "You used to make your living as a hunter, guide, or tracker. Let's see if you can hunt down a guide to get you off of this track."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(377) + " Bow")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(378) + " Arrow x10")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(378) + " Poison Arrow x3")   

        elif origin == "Merchant":
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(262))
            desc = "Though not the typical fighting type yourself, you've seen your share of scuffs and challenges. Your ability to swindle and swoon may come in handy."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(372) + " Staff (+1 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(364) + " Merchants Bag (+24 Carrying)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 100 Gold")
            
        elif origin == "Criminal":
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(260))
            desc = "Found you in the seedy underbelly of town.  Doesnt look like you made many friends, I figured you might fit in around here."
            
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(368) + " Dagger (+2 ATK)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(382) + " Fingerless Gloves (+3 SPD)")
            libtcod.console_print_ex(0, 13, 24, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 30 Gold")
            
        elif origin == "Tourist": 
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(256))
            desc= "This is why they say not to travel, just stay at home. You only wanted some time away from home, and now you're someone elses warning story."
        
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(395) + " Cargo Shorts (+8 Carrying)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 10 Gold")

        constants['options_origin'] = origin
        
        libtcod.console_set_default_foreground(0, screen_green)
        if index == 0:
            libtcod.console_print_ex(0, 30, 12, libtcod.BKGND_SET, libtcod.CENTER, origin)
            
      
            
        libtcod.console_set_default_foreground(0, screen_lightgray)

        description_lines = textwrap.wrap("  " + desc, 36)               #description for display in the inventory system
        y = 14
        for line in description_lines:
            libtcod.console_print_ex(0, 11, y, libtcod.BKGND_SET, libtcod.LEFT, line)
            y += 1
            
        libtcod.console_flush()

        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:                       
            break
            
        if key.vk == libtcod.KEY_ESCAPE:
            return "nah"
  
            
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            if index == 0:
                if origin == "Adventurer":
                    origin = "Ranger"

                elif origin == "Ranger":
                    origin = "Merchant"

                elif origin == "Merchant":
                    origin = "Criminal"
                    
                elif origin == "Criminal":
                    origin = "Tourist"
      
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            if index == 0:  
                if origin == "Ranger":
                    origin = "Adventurer"

                elif origin == "Merchant":
                    origin = "Ranger"
                    
                elif origin == "Criminal":  
                    origin = "Merchant"
                    
                elif origin == "Tourist":
                    origin = "Criminal"      

def high_score_menu(): #Render the High Scores display
 
    screen_yellow = libtcod.Color(255,255,102)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
       
    key = libtcod.Key()
    mouse = libtcod.Mouse()
            
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_clear(0)

    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, libtcod.black)
           
    libtcod.console_set_default_foreground(0, screen_yellow)
    libtcod.console_print_ex(0, 0, 1, libtcod.BKGND_SET, libtcod.LEFT, "  High Scores   ")     
    libtcod.console_set_default_foreground(0, libtcod.white)

    display = load_high_scores()
    display_name_one = str(display[0])                  # Rank One name     | name      0
    display_score_one = str(display[1])                 # score             | score     1
    display_class_one = str(display[2])                 # class             | name      2
    display_character_level_one = str(display[3])       # level             | score     3
    display_dungeon_level_one = str(display[4])         # dungeon level     | name      4
    display_name_two = str(display[5])                  # Rank Two name     | score     5
    display_score_two = str(display[6])                 # score             | name      6
    display_class_two = str(display[7])                 # class             | score     7
    display_character_level_two = str(display[8])       # level             | name      8
    display_dungeon_level_two = str(display[9])         # dungeon level     | score     9
    display_name_three = str(display[10])               # Rank Three name   | 
    display_score_three = str(display[11])              # score             | 
    display_class_three = str(display[12])              # class             | 
    display_character_level_three = str(display[13])    # level             | 
    display_dungeon_level_three = str(display[14])      # dungeon level     | 
    display_name_four = str(display[15])                # Rank Four name    | 
    display_score_four = str(display[16])               # score             | 
    display_class_four = str(display[17])               # class             | 
    display_character_level_four = str(display[18])     # level             | 
    display_dungeon_level_four = str(display[19])       # dungeon level     | 
    display_name_five = str(display[20])                # Rank Five name    |  
    display_score_five = str(display[21])               # score             | 
    display_class_five = str(display[22])               # class             | 
    display_character_level_five = str(display[23])     # level             | 
    display_dungeon_level_five = str(display[24])       # dungeon level     | 
    
    if display_score_one != '0': #If a score exists to be displayed, do so
        libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "1. " + display_name_one + " the level " + display_character_level_one + " " + display_class_one + ", reached floor " + display_dungeon_level_one)
        libtcod.console_print_ex(0, 5, 4, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_one)
    else: #If not, say so
        libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "1. Empty")
    if display_score_two != '0':
        libtcod.console_print_ex(0, 2, 6, libtcod.BKGND_SET, libtcod.LEFT, "2. " + display_name_two + " the level " + display_character_level_two + " " + display_class_two + ", reached floor " + display_dungeon_level_two)
        libtcod.console_print_ex(0, 5, 7, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_two)
    else:
        libtcod.console_print_ex(0, 2, 6, libtcod.BKGND_SET, libtcod.LEFT, "2. Empty")
    if display_score_three != '0':
        libtcod.console_print_ex(0, 2, 9, libtcod.BKGND_SET, libtcod.LEFT, "3. " + display_name_three + " the level " + display_character_level_three + " " + display_class_three + ", reached floor " + display_dungeon_level_three)
        libtcod.console_print_ex(0, 5, 10, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_three)
    else:
        libtcod.console_print_ex(0, 2, 9, libtcod.BKGND_SET, libtcod.LEFT, "3. Empty")
    if display_score_four != '0':
        libtcod.console_print_ex(0, 2, 12, libtcod.BKGND_SET, libtcod.LEFT, "4. " + display_name_four + " the level " + display_character_level_four + " " + display_class_four + ", reached floor " + display_dungeon_level_four)
        libtcod.console_print_ex(0, 5, 13, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_four)
    else:
        libtcod.console_print_ex(0, 2, 12, libtcod.BKGND_SET, libtcod.LEFT, "4. Empty")
    if display_score_five != '0':
        libtcod.console_print_ex(0, 2, 15, libtcod.BKGND_SET, libtcod.LEFT, "5. " + display_name_five + " the level " + display_character_level_five + " " + display_class_five + ", reached floor " + display_dungeon_level_five)
        libtcod.console_print_ex(0, 5, 16, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_five)
    else:
        libtcod.console_print_ex(0, 2, 15, libtcod.BKGND_SET, libtcod.LEFT, "5. Empty")
    libtcod.console_print_ex(0, 11, 22, libtcod.BKGND_SET, libtcod.LEFT, "yuh")

    libtcod.console_print_ex(0, 2, 26, libtcod.BKGND_SET, libtcod.LEFT, "Enter or Esc to return") 
    libtcod.console_set_default_foreground(0, libtcod.black)    
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)       

        libtcod.console_set_default_foreground(0, screen_lightgray)

        libtcod.console_flush()

        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:                       
            break

        if key.vk == libtcod.KEY_ESCAPE:
            break

def character_name(constants):

    charname = "Player"

    #    if backspace
    #        new_string = left(current_string, len(current_string)-1)
    #    if alpha:
    #        new_string += character
            
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
       
    libtcod.console_set_default_foreground(0, screen_darkgray)
    libtcod.console_print_ex(0, 10, 10, libtcod.BKGND_SET, libtcod.LEFT, "                ") 
    libtcod.console_set_default_foreground(0, screen_yellow)               
    libtcod.console_print_ex(0, 11, 10, libtcod.BKGND_SET, libtcod.LEFT, "Character Name") 
    
    libtcod.console_set_default_foreground(0, screen_blue)
    libtcod.console_print_ex(0, 10, 15, libtcod.BKGND_SET, libtcod.LEFT, "What is the name of our new celebrity?") 
    
    libtcod.console_set_default_foreground(0, screen_yellow)
    libtcod.console_print_ex(0, 29, 17, libtcod.BKGND_SET, libtcod.CENTER, charname)
    
    libtcod.console_set_default_foreground(0, screen_lightgray)
    libtcod.console_print_ex(0, 29, 23, libtcod.BKGND_SET, libtcod.CENTER, "Alphabetical characters only,")
    libtcod.console_print_ex(0, 29, 24, libtcod.BKGND_SET, libtcod.CENTER, "backspace to delete.") 
    
    libtcod.console_set_default_foreground(0, libtcod.white)
    libtcod.console_print_ex(0, 13, 26, libtcod.BKGND_SET, libtcod.LEFT, "Enter to accept, Esc to return") 
    libtcod.console_set_default_foreground(0, libtcod.black)    
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        libtcod.console_set_default_foreground(0, screen_darkgray)
        libtcod.console_print_ex(0, 29, 17, libtcod.BKGND_SET, libtcod.CENTER, "               ")
                    
        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_print_ex(0, 29, 17, libtcod.BKGND_SET, libtcod.CENTER, charname)            
                        
        libtcod.console_flush()

        if key.vk == libtcod.KEY_ESCAPE:
            return "nah"
            
        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:            
            constants['player_name'] = charname
            return True
                
        elif key.vk == libtcod.KEY_BACKSPACE:
            charname = str(left(charname, len(charname)-1)).title()
                
        elif key.c > 96 and key.c < 123:
            charname = str(charname + chr(key.c)).title()
            if len(charname) > 15: charname = left(charname, 15)

def inventory_menu(player, entities, fov_map, names_list, colors_list, message_log, constants):
    
    results = []
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    #Initial Inventory Variables
    index = 0
    itemsperpage = 24
    numitems = len(player.inventory.items)
    numequip = len(player.equipment.list) # - player.equipment.list.count('None')
    currentpage = 1
    sort = constants['options_inventory_sort']
    needs_sort = True
    
    #Make sure there is inventory to display
    if numitems + numequip == 0:
        results.append({'message': Message("Ya' cabbash", libtcod.white)})
        return results


    #print static UI elements
    if True:
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
        
        libtcod.console_print_ex(0, 42, 3, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + str(player.score))
        libtcod.console_print_ex(0, 45, 5, libtcod.BKGND_SET, libtcod.RIGHT, "Helm")
        libtcod.console_print_ex(0, 45, 7, libtcod.BKGND_SET, libtcod.RIGHT, "Armor")
        libtcod.console_print_ex(0, 45, 9, libtcod.BKGND_SET, libtcod.RIGHT, "Accessory")
        
        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_print_ex(0, 2, 2, libtcod.BKGND_SET, libtcod.LEFT, "Inventory")
        
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "[Escape to Close, S to Sort]")   
            
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
   
        numequip = (len(player.equipment.list) - player.equipment.list.count(None))
        numitems = len(player.inventory.items)
        numpages = int((numitems + numequip)/ itemsperpage) + 1
        
        if numitems == 0 and numequip == 0:
            return results
                
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_set_default_background(0, screen_darkgray)
  
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, "                      ")
        libtcod.console_set_default_foreground(0, screen_midgray)
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, "Page " + str(currentpage) + " of " + str(numpages))
        libtcod.console_print_ex(0, 44, 36, libtcod.BKGND_SET, libtcod.LEFT, "Cap. " + str(numitems + numequip) + " of " + str(player.inventory.max_capacity))
        
        libtcod.console_print_ex(0, 26, 5, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        libtcod.console_print_ex(0, 26, 7, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        libtcod.console_print_ex(0, 26, 9, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        libtcod.console_print_ex(0, 47, 5, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        libtcod.console_print_ex(0, 47, 7, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        libtcod.console_print_ex(0, 47, 9, libtcod.BKGND_SET, libtcod.LEFT, "[  None  ]") 
        
        #re-draw (clear) inventory space
        for y in range(13, 13+itemsperpage):
            for x in range(3, 30):
                if y % 2 == 0: #even
                    libtcod.console_set_default_background(0, screen_midgray)
                else: #odd
                    libtcod.console_set_default_background(0, screen_lightgray)
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
        
        #if it needs sorted, sort it.
        if needs_sort:
            needs_sort = False
            if sort == "Power": strkey = "equippable.power_bonus"
            elif sort == "Defense": strkey = "equippable.defense_bonus"
            elif sort == "MaxHP": strkey = "equippable.max_hp_bonus"
            elif sort == "Speed": strkey = "equippable.speed_bonus"
            elif sort == "Luck": strkey = "equippable.luck_bonus"
            elif sort == "Capacity": strkey = "equippable.capacity_bonus"
            elif sort == "Type": strkey = "char"
            else: strkey = "name"

            player.equipment.list = sorted(player.equipment.list, key=myattrgetter(strkey, "name")) 
            player.inventory.items = sorted(player.inventory.items, key=myattrgetter(strkey, "name")) 
            
            if not (sort == "name" or sort == "type"):
                player.equipment.list.reverse()
                player.inventory.items.reverse()
                
        #first inventory row
        y = 13  
        
        #draw items and equipment list
        libtcod.console_set_default_foreground(0, libtcod.black)
       
        #process equipment in inventory list
        if numequip > 0:
            #print in inventory list
            if currentpage == 1:
                for x in range (0 + (itemsperpage * (currentpage-1)), numequip):
                    itm = get_item_at("equipment", currentpage, x, player)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, "> " + get_name_string(itm, names_list))    
                    y += 1
                
            #print in top menu
            (ex, ey) = (0, 0)
            libtcod.console_set_default_background(0, screen_darkgray)
            libtcod.console_set_default_foreground(0, screen_yellow)
            for e in player.equipment.list:
                if (e.equippable.slot) == EquipmentSlots.MAIN_HAND: (ex, ey) = (26, 5)
                elif (e.equippable.slot) == EquipmentSlots.OFF_HAND: (ex, ey) = (26, 7)
                elif (e.equippable.slot) == EquipmentSlots.ACC1: (ex, ey) = (26, 9)
                elif (e.equippable.slot) == EquipmentSlots.HELM: (ex, ey) = (47, 5)
                elif (e.equippable.slot) == EquipmentSlots.ARMOR: (ex, ey) = (47, 7)
                elif (e.equippable.slot) == EquipmentSlots.ACC2: (ex, ey) = (47, 9)
                strname = names_list[e.name]
                if len(strname) > 10: strname = left(strname, 10)
                libtcod.console_print_ex(0, ex, ey, libtcod.BKGND_SET, libtcod.LEFT, "          ") 
                libtcod.console_print_ex(0, ex, ey, libtcod.BKGND_SET, libtcod.LEFT, strname) 
        
        
        #process inventory
        libtcod.console_set_default_foreground(0, libtcod.black)
        if numitems > 0:
            start  = 0 + (itemsperpage * (currentpage-1))
            end = start + itemsperpage
            if currentpage == 1: end -= numequip   
            for x in range (start, end):
                if x < len(player.inventory.items):
                    itm = get_item_at("inventory", currentpage, x, player)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, get_name_string(itm, names_list))    
                    y += 1   
                
        mx = mouse.cx
        my = mouse.cy

        # elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        #     cap = numitems -1
        #     if currentpage == 1: cap += numequip
        #     if index < cap: index += 1
        #     if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        # elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
        #     if index > 0: index -= 1
        #     if line == 13 and currentpage > 1: currentpage -= 1


        #if the mouse is in the right position, use mouseindex
        if my >= 13 and my < (13 + itemsperpage):
            if mx >= 3 and mx < 30:
                mouse_index = my-13
                cap = numitems -1
                if currentpage == 1: cap += numequip
                if mouse_index <= cap: index = mouse_index

        #iindex = index
        #green selection line
        strname = ""
        iindex = index
        if numequip > 0:
            if currentpage == 1:
                if index < numequip: 
                    system = "equipment"
                    strname = "> "
                else:   
                    system = "inventory"
                    iindex = index - numequip
        else:
            system = "inventory"
            iindex = index - numequip
        
        #get the item at the current index
        item = get_item_at(system, currentpage, iindex, player)
        line = 13 + (index%itemsperpage)
        
        #draw the green selection line
        strname += get_name_string(item, names_list)
        libtcod.console_set_default_background(0, screen_green)
        libtcod.console_set_default_foreground(0, libtcod.black)
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_SET, libtcod.LEFT, "                           ")  
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_NONE, libtcod.LEFT, strname)   
        
        #clear the description area
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        for y in range (15, 32):
            libtcod.console_print_ex(0, 44, y, libtcod.BKGND_SET, libtcod.CENTER, "                          ")

        
        libtcod.console_set_default_background(0, screen_midgray)
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, " " + chr(item.char) + " " + names_list[item.name] + " ")
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)

        #get and draw the description
        lines = item.item.description_lines
        
        y = 15
        for l in lines:
            libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
            y+=1           
            
        if item.equippable:
            libtcod.console_set_default_background(0, screen_darkgray)
            libtcod.console_set_default_foreground(0, screen_lightgray)
    
            #if no eq to comapre to, the difference is just the bonus of the item in question
            diff_atk = item.equippable.power_bonus
            diff_def = item.equippable.defense_bonus
            diff_mhp = item.equippable.max_hp_bonus
            diff_spd = item.equippable.speed_bonus
            diff_lck = item.equippable.luck_bonus
            diff_cap = item.equippable.capacity_bonus
            
            comp = None
            for eq in player.equipment.list:
                if eq.equippable.slot == item.equippable.slot:
                   comp = eq
                   break
                          
            #if there is eq to compare to, and it's not the same item, list its stats, and the difference is comp - current
            if comp and comp != item:
                
            
                diff_atk = item.equippable.power_bonus - comp.equippable.power_bonus
                diff_def = item.equippable.defense_bonus - comp.equippable.defense_bonus
                diff_mhp = item.equippable.max_hp_bonus - comp.equippable.max_hp_bonus
                diff_spd = item.equippable.speed_bonus - comp.equippable.speed_bonus 
                diff_lck = item.equippable.luck_bonus - comp.equippable.luck_bonus
                diff_cap = item.equippable.capacity_bonus - comp.equippable.capacity_bonus
                
                #print the comp stats
                if True:
                    x = 45
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    
                    libtcod.console_print_ex(0, x, y+2, libtcod.BKGND_SET, libtcod.LEFT, comp.name)
                    libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "ATK 00")
                    libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "DEF 00")
                    libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "MHP 00")
                    libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "SPD 00")
                    libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "LCK 00")
                    libtcod.console_print_ex(0, x, y+9, libtcod.BKGND_SET, libtcod.LEFT, "CAP 00")
                    
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.power_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.defense_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.max_hp_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.speed_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.luck_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+9, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.capacity_bonus))
                    
            x = 41
            if comp and comp != item: x = 37
            
            libtcod.console_print_ex(0, x, y+2, libtcod.BKGND_SET, libtcod.LEFT, item.name)
            libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "ATK 00")
            libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "DEF 00")
            libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "MHP 00")
            libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "SPD 00")
            libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "LCK 00")
            libtcod.console_print_ex(0, x, y+9, libtcod.BKGND_SET, libtcod.LEFT, "CAP 00")

            #print the item stats    
            if True:

                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.power_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.defense_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.max_hp_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.speed_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.luck_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+9, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.capacity_bonus))
            
        if names_list[item.name] == item.name: #only write the effect if its identified    
            if item.item.effect_lines:
                y += 1 #start the effect text after the description text ends.
                for l in item.item.effect_lines:
                    libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
                    y+=1  
                
        #re-draw (clear) possible action items
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_print_ex(0, 31, 32, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to use or (d)equip")
        libtcod.console_print_ex(0, 31, 34, libtcod.BKGND_SET, libtcod.LEFT, "[A]pply [D]rop [T]hrow")
        
        #draw relevant action items
        libtcod.console_set_default_foreground(0, libtcod.light_green)
        libtcod.console_print_ex(0, 39, 34, libtcod.BKGND_SET, libtcod.LEFT, "[D]rop")
        if (item.item and item.item.use_function) or item.equippable: libtcod.console_print_ex(0, 31, 32, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to use or (d)equip")
        
        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)    

        left_click = mouse.lbutton_pressed

        if key.vk == libtcod.KEY_ESCAPE or chr(key.c) == "i":
            #results.append({'ignore': 0})
            return results
            
        elif chr(key.c) == "s":
            sort = sort_menu()
            constants['options_inventory_sort'] = sort
            libtcod.console_clear(0)
            #reprint static UI elements
            if True:
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
                libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "[Escape to Close, S to Sort]")   
             
            needs_sort = True
            
        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER or left_click: 
            
            # if left_click:
            #     if not (my >= 13 and my < (13 + itemsperpage)): break
            #     if not(mx >= 3 and mx < 30): break

            if item.item.use_function:
                use = None
                if item.name == 'Quiver':
                    use = False
                    ammo_list = []
                    for i in player.inventory.items:
                        if i.item.ammo:
                            ammo_list.append(i.name)

                    if len(ammo_list) == 0:
                        print('no ammo')
                    else:
                        use = True
                
                print(str(use))
                if use == None or use == True:
                    results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list, colors_list=colors_list, constants=constants)) 
                    return results 
                
            elif item.equippable:
                #player.equipment.toggle_equip(item)
                equip_results = player.equipment.toggle_equip(item)
                currentpage = 1
                index = 0
                
                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        player.inventory.remove_item(equipped)
                        #message_log.add_message(Message('You equipped the {0}.'.format(equipped.name)))
                        

                    if dequipped:
                        # TODO if the item in question has a capacity bonus
                        #   then if removing that capacity bonus puts player over capacity
                        #       do not allow them to remove it

                        player.inventory.add_item(dequipped, names_list)
                        #message_log.add_message(Message('You dequipped the {0}.'.format(dequipped.name)))
            
                    needs_sort = True
            else:
                print("Not sure what to do here? Menu line 1297 ... key enter on a non-usable, non-equippable item?")
                
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            cap = numitems -1
            if currentpage == 1: cap += numequip
            if index < cap: index += 1
            if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            if index > 0: index -= 1
            if line == 13 and currentpage > 1: currentpage -= 1
  
        elif chr(key.c) == "d":
            (item.x, item.y) = (player.x, player.y)
            entities.append(item)
            index = 0 
            currentpage = 1
            if system == "inventory":
                player.inventory.items.remove(item)
            elif system == "equipment":
                player.equipment.list.remove(item)
            else: 
                print("dafuq? " + str(system)) 

def sort_menu():
    
    sort = "Alphabetical"
    index = 0
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    #print static UI elements
    if True:
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_clear(0)
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, libtcod.black)

        #background
        for y in range (16, 24):
            for x in range (20, 41):
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")

        #lines
        for x in range(20, 41):
            libtcod.console_print_ex(0, x, 16, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
            libtcod.console_print_ex(0, x, 23, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
            
        for y in range(16, 24):
            libtcod.console_print_ex(0, 20, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
            libtcod.console_print_ex(0, 40, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
              
        #corners
        libtcod.console_print_ex(0, 20, 16, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
        libtcod.console_print_ex(0, 40, 16, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
        libtcod.console_print_ex(0, 20, 23, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
        libtcod.console_print_ex(0, 40, 23, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
      
        libtcod.console_print_ex(0, 21, 18, libtcod.BKGND_SET, libtcod.LEFT, "Sort Inventory on..")   
        
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 30, 22, libtcod.BKGND_SET, libtcod.CENTER, "[Enter to Accept]")   
            
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_set_default_background(0, screen_darkgray)
        
        libtcod.console_print_ex(0, 21, 20, libtcod.BKGND_SET, libtcod.LEFT, "                   ")

        if index == 0: sort = "Alphabetical"
        elif index == 1: sort = "Type"
        elif index == 2: sort = "Power"
        elif index == 3: sort = "Defense"
        elif index == 4: sort = "MaxHP"
        elif index == 5: sort = "Speed"
        elif index == 6: sort = "Luck"
        elif index == 7: sort = "Capacity"
        
        libtcod.console_set_default_foreground(0, screen_yellow)
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 30, 20, libtcod.BKGND_SET, libtcod.CENTER, sort)   
                    
        libtcod.console_set_default_foreground(0, screen_green)
        if index < 6: libtcod.console_print_ex(0, 38, 20, libtcod.BKGND_SET, libtcod.CENTER, ">")      
        if index > 0: libtcod.console_print_ex(0, 22, 20, libtcod.BKGND_SET, libtcod.CENTER, "<") 
        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
          
        if key.vk == libtcod.KEY_ENTER:
            return sort

        elif key.vk == libtcod.KEY_LEFT:
            if index > 0: index -= 1
            
        elif key.vk == libtcod.KEY_RIGHT:
            if index < 7: index += 1

            
def get_item_at(system, page, index, player):

    numequip = len(player.equipment.list) #- player.equipment.list.count(None))
    numitems = len(player.inventory.items) #+ numequip

    itm = None

    if system == "equipment":
        itm = player.equipment.list[index]
    elif system == "inventory":
        itm = player.inventory.items[index]

        
    return itm

def get_name_string(item, names_list):
    istr = chr(item.char) + " " + names_list[item.name]
    
    if item.item.stackable:
        if item.item.count > 1:
            if len(istr) + 5 > 25:
                istr = left(istr, 20)
              
    if len(istr) > 25: istr = left(istr,25)
    
    if item.name != 'Gold' and item.item.stackable and item.item.count > 1: istr = istr + " (x" + str(item.item.count) + ")"
    
    return istr

    
def OLD_inventory_menu(player, entities, fov_map, names_list, colors_list, message_log, sort):
    
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
        
        numequip = (len(player.equipment.list) - player.equipment.list.count(None))
        numitems = len(player.inventory.items) #+ numequip
        numpages = int(numitems / itemsperpage) + 1
        
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
            
        if item.item.effect_lines:
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
                    results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list, colors_list=colors_list))
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
   
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            if index < numitems-1: index += 1
            if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            if index > 0: index -= 1
            if line == 13 and currentpage > 1: currentpage -= 1
            
        elif key.vk == libtcod.KEY_ENTER:
            if item.item.use_function:
                results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list, colors_list=colors_list))
                return results
                
            elif item.equippable:
                #player.equipment.toggle_equip(item)
                equip_results = player.equipment.toggle_equip(item)
                
                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        player.inventory.remove_item(equipped)
                        #message_log.add_message(Message('You equipped the {0}.'.format(equipped.name)))
                        

                    # TODO :: Check carrying cap after dequipping items ..
                        # if numitems > carrying cap .. gamestate = burdened
                        # if game_state = burdened then can only access inventory
                    if dequipped:
                        player.inventory.add_item(dequipped, names_list)
                        #message_log.add_message(Message('You dequipped the {0}.'.format(dequipped.name)))
                       
        elif chr(key.c) == "d":
            results.extend(player.inventory.drop_item(item))
            return results

def main_menu(con, background_image, screen_width, screen_height):

    libtcod.image_blit_2x(background_image, 0, 0, 0)
    libtcod.console_set_default_foreground(0, libtcod.black)
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 6, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'LIGHTS,')
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 5, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'CAMERA,')
    #libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
    #                         'ACTION!')


    menu(con, '', ['Play a new game', 'Continue last game', 'View high scores', 'Quit'], 24, screen_width, screen_height)

def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP, from {0})'.format(player.fighter.max_hp),
               'Strength (+1 attack, from {0})'.format(player.fighter.power),
               'Agility (+1 defense, from {0})'.format(player.fighter.defense)]

    menu(con, header, options, menu_width, screen_width, screen_height-40)


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
    libtcod.console_print_ex(0, 3, 5, libtcod.BKGND_NONE, libtcod.LEFT, player.character_name + ", Level " + str(player.level.current_level))
    libtcod.console_print_ex(0, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, constants['options_difficulty'] + " " + constants['options_origin'])
    
    libtcod.console_set_default_foreground(0, screen_midgray)
    libtcod.console_print_ex(0, 3, 8, libtcod.BKGND_NONE, libtcod.LEFT, str(player.score) + " Points")
    libtcod.console_print_ex(0, 3, 9, libtcod.BKGND_NONE, libtcod.LEFT, str(player.turn_count) + " Turns")
    libtcod.console_print_ex(0, 3, 10, libtcod.BKGND_NONE, libtcod.LEFT, "Dungeon Level " + str(dungeon_level))
    
    libtcod.console_set_default_background(0, screen_darkgray)
    libtcod.console_set_default_foreground(0, screen_blue)
    libtcod.console_print_ex(0, 32, 28, libtcod.BKGND_NONE, libtcod.LEFT, "ATK.")
    libtcod.console_print_ex(0, 32, 29, libtcod.BKGND_NONE, libtcod.LEFT, "DEF.")
    libtcod.console_print_ex(0, 32, 30, libtcod.BKGND_NONE, libtcod.LEFT, "SPD.")
    
    libtcod.console_print_ex(0, 41, 28, libtcod.BKGND_NONE, libtcod.LEFT, "LCK.")
    libtcod.console_print_ex(0, 41, 29, libtcod.BKGND_NONE, libtcod.LEFT, "****")
    libtcod.console_print_ex(0, 41, 30, libtcod.BKGND_NONE, libtcod.LEFT, "****")
    
    libtcod.console_print_ex(0, 50, 28, libtcod.BKGND_NONE, libtcod.LEFT, "****")
    libtcod.console_print_ex(0, 50, 29, libtcod.BKGND_NONE, libtcod.LEFT, "****")
    libtcod.console_print_ex(0, 50, 30, libtcod.BKGND_NONE, libtcod.LEFT, "****")
    
    libtcod.console_set_default_foreground(0, screen_midgray)
    libtcod.console_print_ex(0, 37, 28, libtcod.BKGND_NONE, libtcod.LEFT, "00")
    libtcod.console_print_ex(0, 37, 29, libtcod.BKGND_NONE, libtcod.LEFT, "00")
    libtcod.console_print_ex(0, 37, 30, libtcod.BKGND_NONE, libtcod.LEFT, "00")
    libtcod.console_print_ex(0, 46, 28, libtcod.BKGND_NONE, libtcod.LEFT, "00")
    libtcod.console_print_ex(0, 46, 29, libtcod.BKGND_NONE, libtcod.LEFT, "--")
    libtcod.console_print_ex(0, 46, 30, libtcod.BKGND_NONE, libtcod.LEFT, "--")
    libtcod.console_print_ex(0, 55, 28, libtcod.BKGND_NONE, libtcod.LEFT, "--")
    libtcod.console_print_ex(0, 55, 29, libtcod.BKGND_NONE, libtcod.LEFT, "--")
    libtcod.console_print_ex(0, 55, 30, libtcod.BKGND_NONE, libtcod.LEFT, "--")
    
    libtcod.console_set_default_foreground(0, screen_blue)
    if player.fighter.power > 0: libtcod.console_print_ex(0, 38, 28, libtcod.BKGND_NONE, libtcod.RIGHT, str(player.fighter.power))
    if player.fighter.defense > 0: libtcod.console_print_ex(0, 38, 29, libtcod.BKGND_NONE, libtcod.RIGHT, str(player.fighter.defense))
    if player.fighter.speed > 0: libtcod.console_print_ex(0, 38, 30, libtcod.BKGND_NONE, libtcod.RIGHT, str(player.fighter.speed))
    if player.fighter.luck > 0: libtcod.console_print_ex(0, 47, 28, libtcod.BKGND_NONE, libtcod.RIGHT, str(player.fighter.luck))
    
    libtcod.console_set_default_foreground(0, screen_blue)
    libtcod.console_print_ex(0, 3, 12, libtcod.BKGND_NONE, libtcod.LEFT, "Conduct")
        
    libtcod.console_set_default_foreground(0, screen_lightgray)
    conduct = ""
    if player.potions_drank == 0: conduct += "Prohibitionist/"
    if player.scrolls_read == 0: conduct += "Illiterate/"
    if player.gold_collected == 0:
        conduct += "Scrooge/"
    elif player.gold_collected > 99:
        conduct += "Essential Worker/"
    elif player.gold_collected > 499:
        conduct += "Up and Coming/"
    elif player.gold_collected > 999:
        conduct += "entrepreneur/"
        
    conducts = conduct.split("/")
    y = 13
    for c in conducts:
        libtcod.console_print_ex(0, 5, y, libtcod.BKGND_NONE, libtcod.LEFT, c)
        y += 1
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        libtcod.console_flush()
                
        if key.vk == libtcod.KEY_ESCAPE or chr(key.c) == "s":
            return results

def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)

def help_menu():
    
    results = []
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text
    
    #print static UI elements
    if True:
        print('Static layout elements go here')
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
        
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        
        print('Dynamic layout elements go here')
        
        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        if key.vk == libtcod.KEY_ESCAPE:
            return results
            
        elif chr(key.c) == "s":
            x = 1

def menu_template():
    
    results = []
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    #corners, T pieces
    # libtcod.console_print_ex(0, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
    # libtcod.console_print_ex(0, 11, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    # libtcod.console_print_ex(0, 11, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    # libtcod.console_print_ex(0, 58, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
    # libtcod.console_print_ex(0, 1, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(199))
    # libtcod.console_print_ex(0, 58, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(182))
    # libtcod.console_print_ex(0, 1, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
    # libtcod.console_print_ex(0, 58, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(188))

    #print static UI elements
    if True:
        print('Static layout elements go here')
        
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
        
        print('Dynamic layout elements go here')
        
        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        
        if key.vk == libtcod.KEY_ESCAPE:
            return results
            
        elif chr(key.c) == "s":
            x = 1
