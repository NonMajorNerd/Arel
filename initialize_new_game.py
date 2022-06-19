#from input_handlers import player_pick_dir
import tcod as libtcod
import _globals
import _items

from random import randint
from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.ammo import Ammo
from ammo_functions import BasicShot, PoisonShot
from components.vendors import vendor_data_loader
from item_functions import use_arrow
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder
from item_functions import use_quiver

def load_customfont():
    #The index of the first custom tile in the file
    a = 256
 
    for y in range(5,20):
        libtcod.console_map_ascii_codes_to_font(a, 32, 0, y)
        a += 32
    
def get_item(item_list, index=0):
    #return a random item from a list, and remove that item from the list.
    
    if len(item_list) == 0: return "oops"
    
    i = randint(0, len(item_list)-1)
    item = item_list[i]
    item_list.remove(item_list[i])
    
    return item    

def get_game_variables(constants, names_list, colors_list):
    
    #Build player entity
    fighter_component = Fighter(hp=100, defense=0, power=1, speed=5)
    inventory_component = Inventory(24)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, 256, libtcod.white, "Player", blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    player.character_name = constants['player_name']
    player.current_gold = 0
    entities = [player]

    #Give the vendor entities stuff to sell
    vendor_data_loader.populate_vendor_inventory()
    #vendor_data_loader.populate__boss_vendor_inventory()

    #Starting Inventory, sprite
    origin = constants['options_origin']
    
    #HEKIN QUIVER
    player.inventory.add_item(_items.quiver, 1)

    if origin == "Adventurer":
        player.char = 256
        
        # #weapons
        # player.equipment.list.append(_items.staff)
        # player.equipment.list.append(_items.sword)
        # player.equipment.list.append(_items.dagger)
        # player.inventory.add_item(_items.bow, 1)
        # player.inventory.add_item(_items.quiver, 1)

        # #consumables
        # player.inventory.add_item(_items.arrow, 100)
        # player.inventory.add_item(_items.psn_arrow, 10)

        # #amor/accessories 
        # player.equipment.list.append(_items.shield)
        # player.equipment.list.append(_items.fingerless_gloves)
        # player.equipment.list.append(_items.cargo_shorts)
        # player.equipment.list.append(_items.merchants_bag)

        #sword
        player.equipment.list.append(_items.sword)
        
        #shield
        player.equipment.list.append(_items.shield)
        
        #10 gold
        player.inventory.add_item(_items.gold, 10)
        
    elif origin == "Ranger":
        player.char = 258
       
        #3x Pos. Arrow
        player.inventory.add_item(_items.psn_arrow, 3)
        
        #10x. Arrow
        player.inventory.add_item(_items.arrow, 10)

        #Bow
        player.equipment.list.append(_items.bow)
        

    elif origin == "Merchant":
        player.char = 260
        #staff
        player.equipment.list.append(_items.staff)
        
        #merchants bag
        player.equipment.list.append(_items.merchants_bag) 
        
        #100 gold
        player.inventory.add_item(_items.gold, 100)
        
    elif origin == "Criminal":
        player.char = 262
        #dagger
        player.equipment.list.append(_items.dagger)
        
        #fingerless gloves
        player.equipment.list.append(_items.fingerless_gloves)  
        
        #30 gold
        player.inventory.add_item(_items.gold, 30)
        
    elif origin == "Tourist":
        player.char = 264
        #cargo shorts
        player.equipment.list.append(_items.cargo_shorts)
        
        #10 gold
        player.inventory.add_item(_items.gold, 10)
        
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, names_list, colors_list)
    
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
