import libtcodpy as libtcod

from components.ai import ConfusedMonster
from fov_functions import initialize_fov
from menus import m1m2_menu
import condition_functions


from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': True, 'message': Message('Nothing seems to happen.', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)                                                                            #heal for ammt                                                    
        results.append({'consumed': True, 'message': Message('Your wounds instantly close!', libtcod.lighter_green)})  #consume item, send message
    
    if entity.name == 'Player': entity.potions_drank += 1  #if this is the player, update potions drank #
    return results

def poison_potion(*args, **kwargs):
    entity = args[0]
    duration = kwargs.get('duration')
    damage = kwargs.get('damage')
    
    results = []
    if entity.name == 'Player': entity.potions_drank += 1  
    
    entity.conditions.append(condition_functions.Poison(target=entity, active=True, duration=duration, damage=damage))
    results.append({'consumed': True, 'message': Message('You feel unwell.', libtcod.lighter_red)})
    
    return results
    
def restore_wounds(*args, **kwargs):
    entity = args[0]
    duration = kwargs.get('duration')
    healing = kwargs.get('healing')
    
    results = []
    if entity.name == 'Player': entity.potions_drank += 1  
    
    entity.conditions.append(condition_functions.Healing(target=entity, active=True, duration=duration, healing=healing))
    results.append({'consumed': True, 'message': Message('Your wounds begin to close.', libtcod.lighter_green)})
    
    return results
    
def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in _globals.entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder!'.format(target.name))})
        results.extend(target.fighter.take_damage(damage))
        if entity.name == 'Player': 
            entity.scrolls_read += 1 
            print("scrolls read : " + str(entity.scrolls_read))                                                     #if this is the player, update scrolls read #
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})
    
    
    for entity in entities:
        if entity.name == 'Player': 
            entity.scrolls_read += 1 
            print("scrolls read : " + str(entity.scrolls_read))
        if entity.distance(target_x, target_y) <= radius:
            if entity.fighter:
                results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
                results.extend(entity.fighter.take_damage(damage))
            elif entity.item and entity.item.flammable:
                results.append({'message': Message('The {0} is destroyed in the fire!'.format(entity.name, damage), libtcod.orange)})
                entities.remove(entity)
    return results

def use_arrow(*args, **kwargs):
    #this function will be assigned to all arrow items
    #when you 'use' an arrow in the inventory, this will be called to assign the preference to the selected arrow
    return 1

def use_quiver(*args, **kwargs):
    player = args[0]
    constants = kwargs.get('constants')

    results = []
    
    ammo_list =[]

    for i in player.inventory.items:
        print(str(i.name))
        if i.item.ammo:
            ammo_list.append(i.name)

    if len(ammo_list) == 0:
        print("quiver used; no ammo")
        return ("nah")

    constants['options_ammo_preference'] = m1m2_menu(x=31, y=21, w=25, h=8, numoptions=8, optionslist=ammo_list)

def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.name == 'Player': 
            entity.scrolls_read += 1 
            print("scrolls read : " + str(entity.scrolls_read))
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} become vacant as it starts to wander about confused!'.format(entity.name), libtcod.light_green)})
        
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
