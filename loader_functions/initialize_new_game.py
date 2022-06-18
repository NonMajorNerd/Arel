#from input_handlers import player_pick_dir
import tcod as libtcod
import _globals
import components.vendors as vendors

from random import randint
from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.ammo import Ammo
from ammo_functions import BasicShot, PoisonShot
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

    #populate the vendors inventory
    vendors.vendor_data_loader.populate_vendor_inventory()

    #Starting Inventory, sprite
    origin = constants['options_origin']
    
    #HEKIN QUIVER
    item_component = Item(use_function=use_quiver, stackable=False, flammable=True,
                    description="A quiver for storing arrows.",
                    effect="Firing preference is currently unassigned.")
    item = Entity(0, 0, 394, _globals.colors_list[names_list['Quiver']], 'Quiver', item=item_component)
    player.inventory.items.append(item)    

    if origin == "Adventurer":
        player.char = 256
        
        #sword
        item_component = Item(use_function=None, stackable=False,
                        description="A short, one-handed sword.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
        item = Entity(0, 0, 369, colors_list[names_list['Sword']], 'Sword', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)       
        
        #shield
        item_component = Item(use_function=None, stackable=False,
                        description="A small, round, metal shield.")
        equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
        item = Entity(0, 0, 375, colors_list[names_list['Shield']], 'Shield', equippable=equippable_component, item=item_component)
        player.equipment.list.append(item)
        
        #10 gold
        item_component = Item(use_function=None, stackable=True, count=20,
               description="Yanno, gold coins! For procuring goods and/or services!")
        item = Entity(0, 0, 365, colors_list[names_list['Gold']], 'Gold', render_order=RenderOrder.ITEM, item=item_component)
        player.inventory.add_item(item)
        player.gold_collected = 20
        player.current_gold = 20
        
    elif origin == "Ranger":
        player.char = 258
       
        #3x Pos. Arrow
        hit_component =  PoisonShot(2, 1, 10)
        ammo_component = Ammo(hit_function=hit_component, retrievable=True)
        item_component = Item(use_function=use_arrow(), stackable=True, count=3, ammo=ammo_component, flammable=True, range=0,
                       description="Poison-coated arrow. Icky!")
        item = Entity(0, 0, 378, colors_list[names_list['Arrow']], 'Poison Arrow', item=item_component)
        player.inventory.items.append(item)    
        
        #10x. Arrow
        hit_component =  BasicShot(2)
        ammo_component = Ammo(hit_function=hit_component, retrievable=True)
        item_component = Item(use_function=None, stackable=True, count=10, ammo=ammo_component, flammable=True, range=0,
                       description="Arrow. Pewpew!")
        item = Entity(0, 0, 378, colors_list[names_list['Arrow']], 'Arrow', item=item_component)
        player.inventory.items.append(item) 

        #Bow
        item_component = Item(use_function=None, stackable=False, flammable=True, ammo=["Arrow", "Poison Arrow"], range=5,
                        description="A small, low-range bow.")
        equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=0)
        item = Entity(0, 0, 377, colors_list[names_list['Short Bow']], 'Short Bow', equippable=equippable_component, item=item_component)
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
        player.current_gold = 100
        
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
        player.current_gold = 30
        
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
        player.current_gold = 10
        
    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, names_list, colors_list)
    
    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
