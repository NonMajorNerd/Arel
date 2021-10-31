#from input_handlers import player_pick_dir
import tcod as libtcod
from random import randint

from tcod.constants import FONT_LAYOUT_TCOD

from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.ammo import Ammo
from ammo_functions import BasicShot, PoisonShot
from item_functions import use_arrow

from condition_functions import Poison, Healing

from entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder

from item_functions import use_quiver
import _globals
global constants
global player

def load_customfont():
    #The index of the first custom tile in the file
    a = 256
 
    for y in range(5,20):
        libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
        a += 32


def get_constants():

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
    options_death_delete_save = True #not a thing
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
        'options_death_delete_save': options_death_delete_save,
        'options_tutorial_enabled': options_tutorial_enabled,
        'options_inventory_sort': options_inventory_sort,
        'options_ammo_preference': options_ammo_preference
    }

    return constants
    
def get_render_colors():
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
    #'Black Potion':                 libtcod.Color(80, 80, 80),
    'Brown Potion':                 libtcod.Color(145, 63, 0),
    #'Azure Potion':                 libtcod.Color(0, 50, 100),
    'Ivory Potion':                 libtcod.Color(100, 100, 94),
    'Teal Potion':                  libtcod.Color(0, 75, 75),
    'Silver Potion':                libtcod.Color(175, 175, 175),
    'Purple Potion':                libtcod.Color(150, 0, 150),
    #'Gray Potion':                  libtcod.Color(120, 120, 120),
    'Orange Potion':                libtcod.Color(100, 65, 0),
    'Maroon Potion':                libtcod.Color(50, 0, 0),
    #'Charcoal Potion':              libtcod.Color(80, 80, 80),
    'Aquamarine Potion':            libtcod.Color(50, 100, 83),
    'Coral Potion':                 libtcod.Color(100, 50, 31),
    'Fuchsia Potion':               libtcod.Color(200, 0, 200),
    #'Crimson Potion':               libtcod.Color(103, 28, 44),
    'Khaki Potion':                 libtcod.Color(94, 90, 55),
    'Magenta Potion':               libtcod.Color(100, 20, 100),
    'Golden Potion':                libtcod.Color(212, 175, 55),
    #'Plum Potion':                  libtcod.Color(87, 63, 87),
    #'Olive Potion':                 libtcod.Color(50, 50, 0),
    'Cyan Potion':                  libtcod.Color(0, 100, 100),
    'Sword':                        libtcod.light_sky,
    'Shield':                       libtcod.darker_orange,
    'Gold':                         libtcod.dark_yellow,
    'Short Bow':                    libtcod.brass,
    'Arrow':                        libtcod.desaturated_amber,
    'Quiver':                       libtcod.desaturated_amber
    }
    
    return colors_list
    
def get_unidentified_names():
    
    potion_colors_list = [    
    'White',
    'Yellow',
    'Blue',
    'Red',
    'Green',
    #'Black',
    'Brown',
    #'Azure',
    'Ivory',
    'Teal',
    'Silver',
    'Purple',
    #'Gray',
    'Orange',
    'Maroon',
    #'Charcoal',
    'Aquamarine',
    'Coral',
    'Fuchsia',
    #'Crimson',
    'Khaki',
    'Magenta',
    'Golden',
    #'Plum',
    #'Olive',
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
    
    names_list = {
    'Junk':                     'Junk',
    'Stairs':                   'Stairs',
    'Player':                   'Player',
    'Targeter':                 'Targeter',
    'Sword':                    'Sword',
    'Shield':                   'Shield',
    'Short Bow':                'Short Bow',
    'Arrow':                    'Arrow',
    'Poison Arrow':              'Poison Arrow',
    'Quiver':                   'Quiver',
    'Camera Op.':               'Camera Op.',
    'rat':                      'rat',
    'rat swarm':                'rat swarm',
    'rat prince':               'rat prince',
    'rat king':                 'rat king',
    'bat':                      'bat',
    'goblin':                   'goblin',
    'Goblin Spear':             'Spear',
    'troll':                    'troll',
    'remains of Camera Op.':    'Remains of Camera Op.',
    'remains of rat':           'Remains of Rat',
    'remains of rat prince':    'Remains of Rat Prince',
    'remains of rat king':      'Remains of Rat King',
    'remains of bat':           'Remains of Bat',
    'remains of goblin':        'Remains of Goblin',
    'remains of troll':         'Remains of Troll',
    'Staff':                    'Staff',
    'Merchants Bag':            'Merchants Bag',
    'Fingerless Gloves':        'Fingerless Gloves',
    'Dagger':                   'Dagger',
    'Gold':                     'Gold',
    'Cargo Shorts':             'Cargo Shorts',
    'Cure Wounds':              (str(get_item(potion_colors_list)) + " Potion"),
    'Restore Wounds':           (str(get_item(potion_colors_list)) + " Potion"),
    'Foul Liquid':              (str(get_item(potion_colors_list)) + " Potion"),
    'Lightning Scroll':         ("Scroll labeled '" + str(get_item(scroll_names_list)) + "'"),
    'Fireball Scroll':          ("Scroll labeled '" + str(get_item(scroll_names_list)) + "'"),
    'Confusion Scroll':         ("Scroll labeled '" + str(get_item(scroll_names_list)) + "'")
    }
    
    return names_list

    
def get_item(item_list, index=0):
    #return a random item from a list, and remove that item from the list.
    
    if len(item_list) == 0: return "oops"
    
    i = randint(0, len(item_list)-1)
    item = item_list[i]
    item_list.remove(item_list[i])
    
    return item
    

def get_game_variables():
    
    #Build player entity
    fighter_component = Fighter(hp=100, defense=0, power=1, speed=5)
    inventory_component = Inventory(24)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, 256, libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    player.character_name = _globals.constants['player_name']
    _globals.entities = [player]

    #Starting Inventory, sprite
    origin = _globals.constants['options_origin']
    
    #HEKIN QUIVER
    item_component = Item(use_function=use_quiver, stackable=False, flammable=True,
                    description="A quiver for storing arrows.",
                    effect="Firing preference is currently unassigned.")
    item = Entity(0, 0, 394, _globals.colors_list[_globals.get_from_dict(_globals.names_list,'Quiver')], 'Quiver', item=item_component)
    player.inventory.items.append(item)    

    if origin == "Adventurer":
        player.char = 256
        
        #sword
        item_component = Item(use_function=None, stackable=False,
                        description="A short, one-handed sword.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
        item = Entity(0, 0, 369, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Sword')], 'Sword', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)       
        
        #shield
        item_component = Item(use_function=None, stackable=False,
                        description="A small, round, metal shield.")
        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
        item = Entity(0, 0, 375, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Shield')], 'Shield', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)
        
        #10 gold
        item_component = Item(use_function=None, stackable=True, count=20,
               description="Yanno, gold coins! For procuring goods and/or services!")
        item = Entity(0, 0, 365, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Gold')], 'Gold', render_order=RenderOrder.ITEM, item=item_component)
        player.inventory.add_item(item)
        player.gold_collected = 20
        
    elif origin == "Ranger":
        player.char = 258
       
        #3x Pos. Arrow
        hit_component =  PoisonShot(2, 1, 10)
        ammo_component = Ammo(hit_function=hit_component, retrievable=True)
        item_component = Item(use_function=use_arrow(), stackable=True, count=3, ammo=ammo_component, flammable=True, range=0,
                       description="Poison-coated arrow. Icky!")
        item = Entity(0, 0, 378, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Arrow')], 'Poison Arrow', item=item_component)
        player.inventory.items.append(item)    
        
        #10x. Arrow
        hit_component =  BasicShot(2)
        ammo_component = Ammo(hit_function=hit_component, retrievable=True)
        item_component = Item(use_function=None, stackable=True, count=10, ammo=ammo_component, flammable=True, range=0,
                       description="Arrow. Pewpew!")
        item = Entity(0, 0, 378, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Arrow')], 'Arrow', item=item_component)
        player.inventory.items.append(item) 

        #Bow
        item_component = Item(use_function=None, stackable=False, flammable=True, ammo=["Arrow", "Poison Arrow"], range=5,
                        description="A small, low-range bow.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=0)
        item = Entity(0, 0, 377, _globals.colors_list[_globals.get_from_dict(_globals.names_list, 'Short Bow')], 'Short Bow', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)       
        

    elif origin == "Merchant":
        player.char = 260
        #staff
        item_component = Item(use_function=None, stackable=False,
                        description="A two-handed (but actually one-handed) wooden staff, perfect for whacking things with.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=1)
        item = Entity(0, 0, 372, libtcod.sky, 'Staff', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)      
        
        #merchants bag
        item_component = Item(use_function=None, stackable=False,
                        description="A large leather satchel with many pockets and reinforced compartments.",
                        effect="Increases carrying capacity by 24.")
        equippable_component = Equippable(EquipmentSlots.ACC1, capacity_bonus=24)
        item = Entity(0, 0, 364, libtcod.darker_orange, 'Merchants Bag', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item) 
        
        #100 gold
        item_component = Item(use_function=None, stackable=True, count=100,
               description="Yanno, gold coins! For procuring goods and/or services!")
        item = Entity(0, 0, 365, libtcod.dark_yellow, 'Gold', render_order=RenderOrder.ITEM, item=item_component)
        player.inventory.add_item(item)
        player.gold_collected = 100
        
    elif origin == "Criminal":
        player.char = 262
        #dagger
        item_component = Item(use_function=None, stackable=False,
                        description="A small, rusty dagger. Probably unsafe to handle.",
                        effect="This thing was made for doing stabs.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
        item = Entity(0, 0, 368, libtcod.sky, 'Dagger', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)       
        
        #fingerless gloves
        item_component = Item(use_function=None, stackable=False,
                        description="These definitely had fingers when they were made, but they don't now.",
                        effect="Increases speed by 3")
        equippable_component = Equippable(EquipmentSlots.ACC1, speed_bonus=3)
        item = Entity(0, 0, 382, libtcod.darker_orange, 'Fingerless Gloves', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)  
        
        #30 gold
        item_component = Item(use_function=None, stackable=True, count=30,
               description="Yanno, gold coins! For procuring goods and/or services!")
        item = Entity(0, 0, 365, libtcod.dark_yellow, 'Gold', render_order=RenderOrder.ITEM, item=item_component)
        player.inventory.add_item(item)
        player.gold_collected = 30
        
    elif origin == "Tourist":
        player.char = 264
        #cargo shorts
        item_component = Item(use_function=None, stackable=False,
                        description="These are more pockets than they are shorts, which you're ok with.",
                        effect="Increases carrying capacity by 8.")
        equippable_component = Equippable(EquipmentSlots.ACC1, capacity_bonus=8)
        item = Entity(0, 0, 395, libtcod.darker_orange, 'Cargo Shorts', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)  
        
        #10 gold
        item_component = Item(use_function=None, stackable=True, count=10,
               description="Yanno, gold coins! For procuring goods and/or services!")
        item = Entity(0, 0, 365, libtcod.dark_yellow, 'Gold', render_order=RenderOrder.ITEM, item=item_component)
        player.inventory.add_item(item)
        player.gold_collected = 10
        
    game_map = GameMap(_globals.constants['map_width'], _globals.constants['map_height'])
    game_map.make_map(player)
   

    
    message_log = MessageLog(_globals.constants['message_x'], _globals.constants['message_width'], _globals.constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, _globals.entities, game_map, message_log, game_state
