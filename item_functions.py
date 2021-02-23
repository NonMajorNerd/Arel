import libtcodpy as libtcod

from components.ai import ConfusedMonster
from fov_functions import initialize_fov

from game_messages import Message


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)                                                                                 #heal for ammt  
        if entity.name == 'Player': entity.potions_drank += 1                                                       #if this is the player, update potions drank #
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})  #consume item, send message

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

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder!'.format(target.name))})
        results.extend(target.fighter.take_damage(damage))
        if entity.name == 'Player': entity.scrolls_read += 1                                                          #if this is the player, update scrolls read #
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
        if entity.name == 'Player': entity.scrolls_read += 1      #if this is the player, update scrolls read   TODO :: Change this so it only does this when the player uses this scroll .... wait is this needed??
        if entity.distance(target_x, target_y) <= radius:
            if entity.fighter:
                results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
                results.extend(entity.fighter.take_damage(damage))
            elif entity.item and entity.item.flammable:
                #TODO :: Fix unidentified items displaying identified name when burned this way
                results.append({'message': Message('The {0} is destroyed in the fire!'.format(entity.name, damage), libtcod.orange)})
                entities.remove(entity)
    return results


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
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} become vacant as it starts to wander about confused!'.format(entity.name), libtcod.light_green)})
        
            if entity.name == 'Player': entity.scrolls_read += 1                                                          #if this is the player, update scrolls read #
        
            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.yellow)})

    return results
