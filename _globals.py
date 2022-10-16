#https://stackoverflow.com/questions/13034496/using-global-variables-between-files
import tcod as libtcod
import random
import _items

from entity import Entity
from components.inventory import Inventory
from render_functions import RenderOrder
from components.equipment import Equipment
from components.fighter import Fighter

def init():
    global constants, names_list, comp_names, colors_list, entities, colors, vendorEnt, vendor_inventory, vendor_equipment, vendor_stock_amt, last_item_purchased, amt_purchased

    entities = []

    #globals for vendor usage
    vendor_fighter_component = Fighter(hp=1000, defense=1000, power=1000, speed=1)
    vendorEnt = Entity(1, 1, 388, libtcod.white, 'Vendor', blocks=True, render_order=RenderOrder.TARGETING, fighter=vendor_fighter_component, inventory=Inventory(24), equipment=Equipment(), vendor=True)  
    vendor_stock_amt = 0
    last_item_purchased = " "
    amt_purchased=0

    window_title = "A'Rel"

    screen_width = 60
    screen_height = 40
        
    tick = 0
    tick_speed = 4

    bar_width = 20
    panel_height = 4
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 60
    map_height = screen_height - panel_height

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 10

    max_monsters_per_room = 3
    max_items_per_room = 200
    
    xp_to_score_ratio = 0.05
    kill_seen_by_camera_mult = 4
    
    options_difficulty = "Standard"
    options_origin = "Adventurer"
    options_enemy_damage_scale = 100
    options_player_damage_scale = 100
    options_xp_multiplier = 1
    options_luck_scale = 100
    options_tutorial_enabled = True
    options_inventory_sort = "Alpha"
    options_ammo_preference = None #no default ammo selected

    colors = {
        'dark_wall': libtcod.Color(34, 34, 68),
        'dark_ground': libtcod.Color(17, 17, 34),
        'light_wall': libtcod.Color(102, 102, 153),
        'light_ground': libtcod.Color(34, 34, 68)
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'tick': tick,
        'tick_speed': tick_speed,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors,
        'xp_to_score_ratio': xp_to_score_ratio,
        'kill_seen_by_camera_mult': kill_seen_by_camera_mult,
        'player_name': "Player",
        'options_difficulty': options_difficulty,
        'options_origin': options_origin,
        'options_enemy_damage_scale': options_enemy_damage_scale,
        'options_player_damage_scale': options_player_damage_scale,
        'options_xp_multiplier': options_xp_multiplier,
        'options_luck_scale': options_luck_scale,
        'options_tutorial_enabled': options_tutorial_enabled,
        'options_inventory_sort': options_inventory_sort,
        'options_ammo_preference': options_ammo_preference
    }

    colors_list = {
    'Scrolls':                      [
                                    libtcod.Color(255, 236, 158),
                                    libtcod.Color(255, 221, 138),
                                    libtcod.Color(225, 173, 109),
                                    libtcod.Color(201, 145, 87),
                                    libtcod.Color(210, 170, 119)
                                    ],
    'White Potion':                 libtcod.Color(255, 255, 255),
    'Yellow Potion':                libtcod.Color(255, 255, 0),
    'Blue Potion':                  libtcod.Color(0, 0, 255),
    'Red Potion':                   libtcod.Color(255, 0, 0),
    'Green Potion':                 libtcod.Color(0, 255, 0),
    'Brown Potion':                 libtcod.Color(145, 63, 0),
    'Ivory Potion':                 libtcod.Color(100, 100, 94),
    'Teal Potion':                  libtcod.Color(0, 75, 75),
    'Silver Potion':                libtcod.Color(175, 175, 175),
    'Purple Potion':                libtcod.Color(150, 0, 150),
    'Orange Potion':                libtcod.Color(100, 65, 0),
    'Maroon Potion':                libtcod.Color(50, 0, 0),
    'Aquamarine Potion':            libtcod.Color(50, 100, 83),
    'Coral Potion':                 libtcod.Color(100, 50, 31),
    'Fuchsia Potion':               libtcod.Color(200, 0, 200),
    'Khaki Potion':                 libtcod.Color(94, 90, 55),
    'Magenta Potion':               libtcod.Color(100, 20, 100),
    'Golden Potion':                libtcod.Color(212, 175, 55),
    'Cyan Potion':                  libtcod.Color(0, 100, 100),
    'Sword':                        libtcod.light_sky,
    'Shield':                       libtcod.darker_orange,
    'Gold':                         libtcod.dark_yellow,
    'Bow':                          libtcod.brass,
    'Arrow':                        libtcod.desaturated_amber,
    'Quiver':                       libtcod.desaturated_amber,
    'Debugger Lanyard':             libtcod.white
    }
    
    potion_colors_list = [    
    'White',
    'Yellow',
    'Blue',
    'Red',
    'Green',
    'Brown',
    'Ivory',
    'Teal',
    'Silver',
    'Purple',
    'Orange',
    'Maroon',
    'Aquamarine',
    'Coral',
    'Fuchsia',
    'Khaki',
    'Magenta',
    'Golden',
    'Cyan'
    ]
    
    scroll_names_list = [
    "FOO",
    "UBAR",
    "NR 9",
    "JAPE",
    "ODOG",
    "FREY",
    "MACK",
    "RBDKY", 
    "DNGD",
    "NTHK",
    "YREJ",
    "ETAN",
    "KIAL",
    "REBE"
    ]
    
    random.shuffle(potion_colors_list)
    random.shuffle(scroll_names_list)
    
    names_list = {
    'Junk':                     'Junk',
    'Stairs':                   'Stairs',
    'Player':                   'Player',
    'Targeter':                 'Targeter',
    'Sword':                    'Sword',
    'Shield':                   'Shield',
    'Bow':                      'Bow',
    'Arrow':                    'Arrow',
    'Poison Arrow':             'Poison Arrow',
    'Quiver':                   'Quiver',
    'Vendor':                   'Vendor',
    'Camera Op.':               'Camera Op.',
    'rat':                      'rat',
    'rat swarm':                'rat swarm',
    'rat prince':               'rat prince',
    'rat king':                 'rat king',
    'bat':                      'bat',
    'goblin':                   'goblin',
    'Goblin Spear':             'Goblin Spear',
    'troll':                    'troll',
    'remains of Camera Op.':    'Remains of Camera Op.',
    'remains of rat':           'Remains of Rat',
    'remains of rat prince':    'Remains of Rat Prince',
    'remains of rat king':      'Remains of Rat King',
    'remains of bat':           'Remains of Bat',
    'remains of goblin':        'Remains of Goblin',
    'remains of troll':         'Remains of Troll',
    'Staff':                    'Staff',
    'Merchants Bag':            "Merchant's Bag",
    'Fingerless Gloves':        'Fingerless Gloves',
    'Dagger':                   'Dagger',
    'Gold':                     'Gold',
    'Cargo Shorts':             'Cargo Shorts',
    'Debugger Lanyard':         'Debugger Lanyard',
    'Cure Wounds':              (str(potion_colors_list.pop()) + " Potion"),
    'Restore Wounds':           (str(potion_colors_list.pop()) + " Potion"),
    'Foul Liquid':              (str(potion_colors_list.pop()) + " Potion"),
    'Lightning Scroll':         ("Scroll labeled '" + str(scroll_names_list.pop()) + "'"),
    'Fireball Scroll':          ("Scroll labeled '" + str(scroll_names_list.pop()) + "'"),
    'Confusion Scroll':         ("Scroll labeled '" + str(scroll_names_list.pop()) + "'")
    }

    comp_names = {
        'Staff':                    'Staff',
        'Merchants Bag':            'Bag',
        'Fingerless Gloves':        'Gloves',
        'Dagger':                   'Dagger',
        'Gold':                     'Gold',
        'Cargo Shorts':             'Shorts',
        'Debugger Lanyard':         'Lanyard',
        'Sword':                    'Sword',
        'Shield':                   'Shield',
        'Bow':                      'Bow',
        'Arrow':                    'Arrow',
        'Poison Arrow':             'Poison Arrow',
        'Quiver':                   'Quiver',
        'Goblin Spear':             'Goblin Spear',

    }

    #populate the vendors inventory
    _items.init()
    #vendor_data_loader.populate_vendor_inventory()

def get_from_dict(dict, key):
    if key in dict.keys():
        return dict[key]
    else:
        return key

def load_customfont():
    #The index of the first custom tile in the file
    a = 256
 
    for y in range(5,20):
        libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
        a += 32