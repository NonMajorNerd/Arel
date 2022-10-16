from numpy import SHIFT_DIVIDEBYZERO
import tcod as libtcod
import textwrap
import operator
import _globals

from game_messages import Message
from scoreboard_functions import load_high_scores
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

def intro():

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

def game_options():
 
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
        if _globals.constants['options_tutorial_enabled']: strtut = "Enabled"
        
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
            libtcod.console_print_ex(0, 34, 16, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_enemy_damage_scale']) + "%")
            libtcod.console_print_ex(0, 32, 18, libtcod.BKGND_SET, libtcod.RIGHT, "Player Damage:")
            libtcod.console_print_ex(0, 34, 18, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_player_damage_scale']) + "%")
            libtcod.console_print_ex(0, 32, 20, libtcod.BKGND_SET, libtcod.RIGHT, "Experience Multiplier:") 
            libtcod.console_print_ex(0, 34, 20, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_xp_multiplier']) + "x")
            libtcod.console_print_ex(0, 32, 22, libtcod.BKGND_SET, libtcod.RIGHT, "Luck Scale:") 
            libtcod.console_print_ex(0, 34, 22, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_luck_scale']) + "%")
            #libtcod.console_print_ex(0, 32, 24, libtcod.BKGND_SET, libtcod.RIGHT, "Delete Save on Death:") 
            #strdel = "No"
            #if constants['options_death_delete_save']: strdel = "Yes"
            #libtcod.console_print_ex(0, 34, 24, libtcod.BKGND_SET, libtcod.LEFT, strdel)
        
        libtcod.console_set_default_foreground(0, screen_green)
        if index == 1:
            strtut = "Disabled"
            if _globals.constants['options_tutorial_enabled']: strtut = "Enabled"
            libtcod.console_print_ex(0, 32, 14, libtcod.BKGND_SET, libtcod.RIGHT, "Tutorial Tips:")
            libtcod.console_print_ex(0, 34, 14, libtcod.BKGND_SET, libtcod.LEFT, strtut)
            
        elif index == 2:
            libtcod.console_print_ex(0, 32, 16, libtcod.BKGND_SET, libtcod.RIGHT, "Enemy Damage:")
            libtcod.console_print_ex(0, 34, 16, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_enemy_damage_scale']) + "%")
            
        elif index == 3:
            libtcod.console_print_ex(0, 32, 18, libtcod.BKGND_SET, libtcod.RIGHT, "Player Damage:")
            libtcod.console_print_ex(0, 34, 18, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_player_damage_scale']) + "%")
            
        elif index == 4:
            libtcod.console_print_ex(0, 32, 20, libtcod.BKGND_SET, libtcod.RIGHT, "Experience Multiplier:")
            libtcod.console_print_ex(0, 34, 20, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_xp_multiplier']) + "x")
            
        elif index == 5:
            libtcod.console_print_ex(0, 32, 22, libtcod.BKGND_SET, libtcod.RIGHT, "Luck Scale:")
            libtcod.console_print_ex(0, 34, 22, libtcod.BKGND_SET, libtcod.LEFT, str(_globals.constants['options_luck_scale']) + "%")
            
            
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
                _globals.constants['options_enemy_damage_scale'] = 80
                _globals.constants['options_player_damage_scale'] = 120
                _globals.constants['options_xp_multiplier'] = round(1.5, 1)
                _globals.constants['options_luck_scale'] = 150
                #constants['options_death_delete_save'] = False
                
            elif difficulty == "Classic":
                _globals.constants['options_enemy_damage_scale'] = 100
                _globals.constants['options_player_damage_scale'] = 100
                _globals.constants['options_xp_multiplier'] = 1
                _globals.constants['options_luck_scale'] = 100
                #constants['options_death_delete_save'] = True
                
            elif difficulty == "Expert":
                _globals.constants['options_enemy_damage_scale'] = 130
                _globals.constants['options_player_damage_scale'] = 70
                _globals.constants['options_xp_multiplier'] = round(.5, 1)
                _globals.constants['options_luck_scale'] = 75
                #constants['options_death_delete_save'] = True
                
            elif difficulty == "Sadist":
                _globals.constants['options_enemy_damage_scale'] = 200
                _globals.constants['options_player_damage_scale'] = 30
                _globals.constants['options_xp_multiplier'] = round(.1, 1)
                _globals.constants['options_luck_scale'] = 30
                #constants['options_death_delete_save'] = True
                
            _globals.constants['options_difficulty'] = difficulty
                
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
                _globals.constants['options_tutorial_enabled'] = not _globals.constants['options_tutorial_enabled']
            if index == 2:
                if _globals.constants['options_enemy_damage_scale'] < 990: _globals.constants['options_enemy_damage_scale'] += 10
            if index == 3:
                if _globals.constants['options_player_damage_scale'] < 990: _globals.constants['options_player_damage_scale'] += 10       
            if index == 4:
                if _globals.constants['options_xp_multiplier'] < 100:
                    if key.shift:
                        _globals.constants['options_xp_multiplier'] += 10
                    else:
                        _globals.constants['options_xp_multiplier'] = round(_globals.constants['options_xp_multiplier']+ 0.2, 1)
                    if _globals.constants['options_xp_multiplier'] > 100: _globals.constants['options_xp_multiplier'] = 100
            if index == 5:
                if _globals.constants['options_luck_scale'] < 990: _globals.constants['options_luck_scale'] += 10   
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
                _globals.constants['options_tutorial_enabled'] = not _globals.constants['options_tutorial_enabled']
            if index == 2:
                if _globals.constants['options_enemy_damage_scale'] > 10: _globals.constants['options_enemy_damage_scale'] -= 10
            if index == 3:
                if _globals.constants['options_player_damage_scale'] > 10: _globals.constants['options_player_damage_scale'] -= 10    
            if index == 4:
                if _globals.constants['options_xp_multiplier'] > 0.2:
                    if key.shift:
                        _globals.constants['options_xp_multiplier'] = round(_globals.constants['options_xp_multiplier'] -10, 1)
                    else:
                        _globals.constants['options_xp_multiplier'] = round(_globals.constants['options_xp_multiplier'] - 0.2, 1)
                    if _globals.constants['options_xp_multiplier'] < 0.2: _globals.constants['options_xp_multiplier'] = 0.2
            if index == 5:
                if _globals.constants['options_luck_scale'] > 10: _globals.constants['options_luck_scale'] -= 10    
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

            
def origin_options():
 
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
            
        if origin != "Debugger":
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
            desc= "This is why they say not to travel, just stay at home. You only wanted some time away from home, and now you're someone else's warning story."
        
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(395) + " Cargo Shorts (+8 Carrying)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 10 Gold")
            
        elif origin == "Debugger": 
            libtcod.console_print_ex(0, 13, 12, libtcod.BKGND_NONE, libtcod.LEFT, chr(260))
            desc= "You know why this is here. Judge me, I'm lazy."
        
            libtcod.console_print_ex(0, 13, 22, libtcod.BKGND_NONE, libtcod.LEFT, chr(364) + " Merchants Bag (+24 Carrying)")
            libtcod.console_print_ex(0, 13, 23, libtcod.BKGND_NONE, libtcod.LEFT, chr(365) + " 100000 Gold")

        _globals.constants['options_origin'] = origin
        
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
                    
                elif origin == "Tourist":
                    origin = "Debugger"
      
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
                    
                elif origin == "Debugger":
                    origin = "Tourist"      

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
    display_name_one = str(display[0])
    display_score_one = str(display[1])
    display_class_one = str(display[2])
    display_character_level_one = str(display[3])
    display_dungeon_level_one = str(display[4])
    display_name_two = str(display[5])
    display_score_two = str(display[6])
    display_class_two = str(display[7])
    display_character_level_two = str(display[8])
    display_dungeon_level_two = str(display[9])
    display_name_three = str(display[10])
    display_score_three = str(display[11])
    display_class_three = str(display[12])
    display_character_level_three = str(display[13])
    display_dungeon_level_three = str(display[14])
    display_name_four = str(display[15])
    display_score_four = str(display[16])
    display_class_four = str(display[17])
    display_character_level_four = str(display[18])
    display_dungeon_level_four = str(display[19])
    display_name_five = str(display[20])
    display_score_five = str(display[21])
    display_class_five = str(display[22])
    display_character_level_five = str(display[23])
    display_dungeon_level_five = str(display[24])
    display_name_six = str(display[25])
    display_score_six = str(display[26])
    display_class_six = str(display[27])
    display_character_level_six = str(display[28])
    display_dungeon_level_six = str(display[29])
    display_name_seven = str(display[30])
    display_score_seven = str(display[31])
    display_class_seven = str(display[32])
    display_character_level_seven = str(display[33])
    display_dungeon_level_seven = str(display[34])
    display_name_eight = str(display[35])
    display_score_eight = str(display[36])
    display_class_eight = str(display[37])
    display_character_level_eight = str(display[38])
    display_dungeon_level_eight = str(display[39])
    display_name_nine = str(display[40])
    display_score_nine = str(display[41])
    display_class_nine = str(display[42])
    display_character_level_nine = str(display[43])
    display_dungeon_level_nine = str(display[44])
    display_name_ten = str(display[45])
    display_score_ten = str(display[46])
    display_class_ten = str(display[47])
    display_character_level_ten = str(display[48])
    display_dungeon_level_ten = str(display[49])
    
    libtcod.console_print_ex(0, 2, 3, libtcod.BKGND_SET, libtcod.LEFT, "1. " + display_name_one + " the level " + display_character_level_one + " " + display_class_one + ", reached floor " + display_dungeon_level_one)
    libtcod.console_print_ex(0, 5, 4, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_one)
    libtcod.console_print_ex(0, 2, 6, libtcod.BKGND_SET, libtcod.LEFT, "2. " + display_name_two + " the level " + display_character_level_two + " " + display_class_two + ", reached floor " + display_dungeon_level_two)
    libtcod.console_print_ex(0, 5, 7, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_two)
    libtcod.console_print_ex(0, 2, 9, libtcod.BKGND_SET, libtcod.LEFT, "3. " + display_name_three + " the level " + display_character_level_three + " " + display_class_three + ", reached floor " + display_dungeon_level_three)
    libtcod.console_print_ex(0, 5, 10, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_three)
    libtcod.console_print_ex(0, 2, 12, libtcod.BKGND_SET, libtcod.LEFT, "4. " + display_name_four + " the level " + display_character_level_four + " " + display_class_four + ", reached floor " + display_dungeon_level_four)
    libtcod.console_print_ex(0, 5, 13, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_four)
    libtcod.console_print_ex(0, 2, 15, libtcod.BKGND_SET, libtcod.LEFT, "5. " + display_name_five + " the level " + display_character_level_five + " " + display_class_five + ", reached floor " + display_dungeon_level_five)
    libtcod.console_print_ex(0, 5, 16, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_five)
    libtcod.console_print_ex(0, 2, 18, libtcod.BKGND_SET, libtcod.LEFT, "6. " + display_name_six + " the level " + display_character_level_six + " " + display_class_six + ", reached floor " + display_dungeon_level_six)
    libtcod.console_print_ex(0, 5, 19, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_six)
    libtcod.console_print_ex(0, 2, 21, libtcod.BKGND_SET, libtcod.LEFT, "7. " + display_name_seven + " the level " + display_character_level_seven + " " + display_class_seven + ", reached floor " + display_dungeon_level_seven)
    libtcod.console_print_ex(0, 5, 22, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_seven)
    libtcod.console_print_ex(0, 2, 24, libtcod.BKGND_SET, libtcod.LEFT, "8. " + display_name_eight + " the level " + display_character_level_eight + " " + display_class_eight + ", reached floor " + display_dungeon_level_eight)
    libtcod.console_print_ex(0, 5, 25, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_eight)
    libtcod.console_print_ex(0, 2, 27, libtcod.BKGND_SET, libtcod.LEFT, "9. " + display_name_nine + " the level " + display_character_level_nine + " " + display_class_nine + ", reached floor " + display_dungeon_level_nine)
    libtcod.console_print_ex(0, 5, 28, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_nine)
    libtcod.console_print_ex(0, 2, 30, libtcod.BKGND_SET, libtcod.LEFT, "10. " + display_name_ten + " the level " + display_character_level_ten + " " + display_class_ten + ", reached floor " + display_dungeon_level_ten)
    libtcod.console_print_ex(0, 5, 31, libtcod.BKGND_SET, libtcod.LEFT, "Score: " + display_score_ten)
    #libtcod.console_print_ex(0, 11, 22, libtcod.BKGND_SET, libtcod.LEFT, "yuh")

    libtcod.console_print_ex(0, 2, 34, libtcod.BKGND_SET, libtcod.LEFT, "Enter or Esc to return") 
    libtcod.console_set_default_foreground(0, libtcod.black)    
    
    while True:
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)       

        libtcod.console_set_default_foreground(0, screen_lightgray)

        libtcod.console_flush()

        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER:                       
            break

        if key.vk == libtcod.KEY_ESCAPE:
            break

def character_name():

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
            _globals.constants['player_name'] = charname
            return True
                
        elif key.vk == libtcod.KEY_BACKSPACE:
            charname = str(left(charname, len(charname)-1)).title()
                
        elif key.c > 96 and key.c < 123:
            charname = str(charname + chr(key.c)).title()
            if len(charname) > 15: charname = left(charname, 15)

def inventory_menu(player, message_log, fov_map):
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
    sort = _globals.constants['options_inventory_sort']
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
        
        libtcod.console_set_default_foreground(0, libtcod.light_flame)
        if player.current_gold <= 100000: libtcod.console_print_ex(0, 42, 3, libtcod.BKGND_SET, libtcod.LEFT, "Gold: " + str(player.current_gold) + "g")
        else: libtcod.console_print_ex(0, 42, 3, libtcod.BKGND_SET, libtcod.LEFT, "Gold: +100000g ")
        libtcod.console_set_default_foreground(0, screen_blue)

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
                    itm = get_item_at("equipment", x, player)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, "> " + get_name_string(itm, _globals.names_list))    
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
                strname = _globals.comp_names[e.name]
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
                    itm = get_item_at("inventory", x, player)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, get_name_string(itm, _globals.names_list))    
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
        item = get_item_at(system, iindex, player)
        line = 13 + (index%itemsperpage)
        
        #draw the green selection line
        strname += get_name_string(item, _globals.names_list)
        libtcod.console_set_default_background(0, screen_green)
        libtcod.console_set_default_foreground(0, libtcod.black)
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_SET, libtcod.LEFT, "                           ")  
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_NONE, libtcod.LEFT, strname + " x" + str(item.item.count))
        
        #clear the description area
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        for y in range (15, 32):
            libtcod.console_print_ex(0, 44, y, libtcod.BKGND_SET, libtcod.CENTER, "                          ")

        
        libtcod.console_set_default_background(0, screen_midgray)
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, " " + chr(item.char) + " " + _globals.names_list[item.name] + " ")
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)

        #get and draw the description
        lines = item.item.description_lines
        
        y = 15
        for l in lines:
            libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
            y+=1           
            
        if _globals.names_list[item.name] == item.name: #only write the effect if its identified    
            if item.item.effect_lines:
                y += 1 #start the effect text after the description text ends.
                for l in item.item.effect_lines:
                    libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
                    y+=1  
                #y += 1
            
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

            comp_total = 0
            item_total = 0

            #if there is eq to compare to, and it's not the same item, list its stats, and the difference is comp - current
            if comp and comp != item:
                x = 45                
            
                diff_atk = item.equippable.power_bonus - comp.equippable.power_bonus
                diff_def = item.equippable.defense_bonus - comp.equippable.defense_bonus
                diff_mhp = item.equippable.max_hp_bonus - comp.equippable.max_hp_bonus
                diff_spd = item.equippable.speed_bonus - comp.equippable.speed_bonus 
                diff_lck = item.equippable.luck_bonus - comp.equippable.luck_bonus
                diff_cap = item.equippable.capacity_bonus - comp.equippable.capacity_bonus
                item_total = (item.equippable.power_bonus + item.equippable.defense_bonus + 
                    item.equippable.max_hp_bonus + item.equippable.speed_bonus + item.equippable.luck_bonus + item.equippable.capacity_bonus) 
                comp_total = (comp.equippable.power_bonus + comp.equippable.defense_bonus + 
                    comp.equippable.max_hp_bonus + comp.equippable.speed_bonus + comp.equippable.luck_bonus + comp.equippable.capacity_bonus) 

                if item_total > comp_total:
                    libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    libtcod.console_print_ex(0, 37, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
                    libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, comp.item.comp_name)
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                
                elif item_total < comp_total:
                    libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, comp.item.comp_name)
                    libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, 37, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                
                #print the comp stats
                if True:
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    libtcod.console_print_ex(0, x, y+3, libtcod.BKGND_SET, libtcod.LEFT, "ATK  ")
                    libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "DEF  ")
                    libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "MHP  ")
                    libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "SPD  ")
                    libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "LCK  ")
                    libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "CAP  ")
                    
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+3, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.power_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.defense_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.max_hp_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.speed_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.luck_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.capacity_bonus))
                    
            x = 41
            if comp and comp != item: x = 37
            
            if item_total > comp_total:
                libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
            elif item_total < comp_total:
                libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
            else:
                libtcod.console_set_default_foreground(0, screen_lightgray)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)

            libtcod.console_set_default_foreground(0, screen_lightgray)
            libtcod.console_print_ex(0, x, y+3, libtcod.BKGND_SET, libtcod.LEFT, "ATK ")
            libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "DEF ")
            libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "MHP ")
            libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "SPD ")
            libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "LCK ")
            libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "CAP ")

            #print the item stats    
            if True:

                    adjusted = False
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_atk >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+3, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.power_bonus))
                    if adjusted: x -= 1; adjusted = False
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_def >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.defense_bonus))
                    if adjusted: x -= 1; adjusted = False
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_mhp >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.max_hp_bonus))
                    if adjusted: x -= 1; adjusted = False
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_spd >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.speed_bonus))
                    if adjusted: x -= 1; adjusted = False
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_lck >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.luck_bonus))
                    if adjusted: x -= 1; adjusted = False
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    if diff_cap >= 100: x +=1; adjusted = True
                    libtcod.console_print_ex(0, x+5, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.capacity_bonus))
                    if adjusted: x -= 1; adjusted = False
                
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
            _globals.constants['options_inventory_sort'] = sort
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
                    results.extend(player.inventory.use(item, entities=_globals.entities, fov_map=fov_map, names_list=_globals.names_list, colors_list=_globals.colors_list, constants=_globals.constants)) 
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

                        player.inventory.add_item(dequipped, 0)
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
            _globals.entities.append(item)
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

            
def get_item_at(system, index, player):

    numequip = len(player.equipment.list) - player.equipment.list.count(None)
    numitems = len(player.inventory.items) + numequip

    itm = None

    if system == "equipment":
        itm = player.equipment.list[index]
    elif system == "inventory":
        itm = player.inventory.items[index]
    elif system == "stock":                 #note that this branch requires both the 'stock' to be passed to the system variable, as well as 'vendorEnt' to the player variable
        itm = _globals.vendorEnt.inventory.items[index]

        
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

def character_screen(player, dungeon_level):
    
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
    libtcod.console_print_ex(0, 3, 6, libtcod.BKGND_NONE, libtcod.LEFT, _globals.constants['options_difficulty'] + " " + _globals.constants['options_origin'])
    
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