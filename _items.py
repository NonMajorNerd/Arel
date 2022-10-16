import tcod as libtcod
import _globals

from components.item import Item
from components.equippable import Equippable
from components.equipment import EquipmentSlots
from components.ammo import Ammo
from entity import Entity
from render_functions import RenderOrder
from components.ammo import Ammo
from ammo_functions import BasicShot, PoisonShot
from item_functions import use_arrow, use_quiver

#global file for items; equipment, potions, scrolls, etc.

def init():

    global staff, sword, dagger, bow, gold, arrow, psn_arrow, cargo_shorts, fingerless_gloves, merchants_bag, shield, quiver, debugger_lanyard

    #---------------------------weapons-------------------------------------------------------------------------------------------------------------------------------------#

    #staff
    item_component_staff = Item(name='Staff', comp_name = 'Staff', use_function=None, stackable=False, count=1, cost=5, take_at_buy=False,
                description="A two-handed (but actually one-handed) wooden staff, perfect for whacking things with.", 
                effect="Increases Attack by 1")
    equippable_component_staff = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=1)
    staff = Entity(0, 0, 372, libtcod.sky, 'Staff', equippable=equippable_component_staff, item=item_component_staff)

    #sword
    item_component_sword = Item(name='Sword', comp_name = 'Sword', use_function=None, stackable=False, count=1, cost=10, take_at_buy=False,
                description="A short, one-handed sword.", effect="Increases Attack by 3")
    equippable_component_sword = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
    sword = Entity(0, 0, 369, libtcod.white, 'Sword', equippable=equippable_component_sword, item=item_component_sword)
        
    #gold
    item_component_gold = Item(use_function=None, stackable=True, count=1,
            description="Yanno, gold coins! For procuring goods and/or services!")
    gold = Entity(0, 0, 365, libtcod.dark_yellow, 'Gold', render_order=RenderOrder.ITEM, item=item_component_gold)
        
    #dagger
    item_component_dagger = Item(name='Dagger',  comp_name = 'Dagger', use_function=None, stackable=False, cost=5, take_at_buy=False,
                description="A small, rusty dagger. Probably unsafe to handle.", effect="Increases A2ttack by 2")
    equippable_component_dagger = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(0, 0, 368, libtcod.sky, 'Dagger', equippable=equippable_component_dagger, item=item_component_dagger)

    #bow
    item_component_bow = Item(name='Bow', comp_name='Bow', use_function=None, stackable=False, flammable=True, ammo=["Arrow", "Poison Arrow"], range=5, cost=10, take_at_buy=False,
                description="A small, low-range bow.", effect="Can be used to fire projectiles at enemies.")
    equippable_component_bow = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=0)
    bow = Entity(0, 0, 377, _globals.colors_list[_globals.names_list['Bow']], 'Bow', equippable=equippable_component_bow, item=item_component_bow)
        
    #arrow
    hit_component_arrow =  BasicShot(2)
    ammo_component_arrow = Ammo(hit_function=hit_component_arrow, retrievable=True)
    item_component_arrow = Item(name='Arrow', comp_name='Arrow', use_function=None, stackable=True, count=1, ammo=ammo_component_arrow, flammable=True, range=0, cost=1,
                    description="Arrow. Pewpew!")
    arrow = Entity(0, 0, 378, _globals.colors_list[_globals.names_list['Arrow']], 'Arrow', item=item_component_arrow)    
       
    #poison arrow
    hit_component_psn_arrow =  PoisonShot(2, 1, 10)
    ammo_component_psn_arrow = Ammo(hit_function=hit_component_psn_arrow, retrievable=True)
    item_component_psn_arrow = Item(name='Poisoned Arrow', comp_name='P. Arrow', use_function=use_arrow(), stackable=True, count=1, ammo=ammo_component_psn_arrow, flammable=True, range=0, cost=5,
                    description="Poison-coated arrow. Icky!")
    psn_arrow = Entity(0, 0, 378, _globals.colors_list[_globals.names_list['Arrow']], 'Poison Arrow', item=item_component_psn_arrow)

    #---------------------------equipment-------------------------------------------------------------------------------------------------------------------------------------#
        
    #shield
    item_component_shield = Item(name='Shield', comp_name='Shield', use_function=None, stackable=False, cost=10, take_at_buy=False,
                    description="A small, round, metal shield.", effect="Increases Defense by 1")
    equippable_component_shield = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
    shield = Entity(0, 0, 375, _globals.colors_list[_globals.names_list['Shield']], 'Shield', equippable=equippable_component_shield, item=item_component_shield)
    
    #HEKIN QUIVER
    item_component_quiver = Item(name='Quiver', comp_name='Quiver', use_function=use_quiver, stackable=False, flammable=True, cost=10, take_at_buy=False,
                    description="A quiver for storing arrows.",
                    effect="Firing preference is currently unassigned.")
    quiver = Entity(0, 0, 394, _globals.colors_list[_globals.names_list['Quiver']], 'Quiver', item=item_component_quiver)
        
    #merchants bag
    item_component_merchants_bag = Item(name="Merchant's Bag", comp_name="Bag", use_function=None, stackable=False, cost=25, take_at_buy=False,
                    description="A large leather satchel with many pockets and reinforced compartments.",
                    effect="Increases carrying capacity by 24.")
    equippable_component_merchants_bag = Equippable(EquipmentSlots.ACC1, capacity_bonus=24)
    merchants_bag = Entity(0, 0, 364, libtcod.darker_orange, 'Merchants Bag', equippable=equippable_component_merchants_bag, item=item_component_merchants_bag)  
        
    #fingerless gloves
    item_component_fingerless_gloves = Item(name='Fingerless Gloves', comp_name='Gloves', use_function=None, stackable=False, cost=5, take_at_buy=False,
                    description="These definitely had fingers when they were made.",
                    effect="Increases speed by 3")
    equippable_component_fingerless_gloves = Equippable(EquipmentSlots.ACC1, speed_bonus=3)
    fingerless_gloves = Entity(0, 0, 382, libtcod.darker_orange, 'Fingerless Gloves', equippable=equippable_component_fingerless_gloves, item=item_component_fingerless_gloves)
        
    #cargo shorts
    item_component_cargo_shorts = Item(name='Cargo Shorts', comp_name='Shorts', use_function=None, stackable=False, cost=10, take_at_buy=False,
                    description="These are more pockets than they are shorts.",
                    effect="Increases carrying capacity by 8.")
    equippable_component_cargo_shorts = Equippable(EquipmentSlots.ACC1, capacity_bonus=8)
    cargo_shorts = Entity(0, 0, 395, libtcod.darker_orange, 'Cargo Shorts', equippable=equippable_component_cargo_shorts, item=item_component_cargo_shorts)

    #debugger lanyard lul
    item_component_debugger_lanyard = Item(name='Debugger Lanyard', comp_name='Lanyard', use_function=None, stackable=False, cost=1, take_at_buy=False,
                    description="You have stuff to do.",
                    effect = "Don't die.")
    equippable_component_debugger_lanyard = Equippable(EquipmentSlots.ACC1, power_bonus=100, defense_bonus=100, max_hp_bonus=100, speed_bonus=100, luck_bonus=100, capacity_bonus=100)
    debugger_lanyard = Entity(0, 0, 365, libtcod.darker_orange, 'Debugger Lanyard', equippable=equippable_component_debugger_lanyard, item=item_component_debugger_lanyard)