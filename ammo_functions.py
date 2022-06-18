import libtcodpy as libtcod
import textwrap
import _globals 

from components.ammo import Ammo
from game_messages import Message
from condition_functions import Poison
from menus import m1m2_menu
#from loader_functions.initialize_new_game import constants, player

def Fire_And_Preference(player=None, constants=None):
    if not _globals.constants: print("Error; ammo_functions line 7.. F&P without constants")
    
    ammo_list =[]

    for i in player.inventory.items:
        if i.item.ammo:
            ammo_list.append(i.name)

    if len(ammo_list) == 0:
        return None

    pref = constants['options_ammo_preference']

    if pref == None:

        numoptions = 4

        #find the longest string in options list to define menu width
        max_len = -1
        for opt in ammo_list:
            if len(opt) > max_len:
                max_len = len(opt)

        w = max_len + 4

        h = numoptions + 3

        x = player.x + 1
        y = player.y - (h+1)
        if x + w >= _globals.constants['screen_width'] -2: x = player.x - (w+2)
        if y < 1: y = 1

        pref = m1m2_menu(x, y, w, h, numoptions, ammo_list)

    if pref != 'exit': _globals.constants['options_ammo_preference'] = pref
    
    for i in player.inventory.items:
        if i.name == 'Quiver':
            if pref == None:
                i.item.effect_lines = textwrap.wrap("  Firing preference is currently unassigned.", 26) 
            else:
                i.item.effect_lines = textwrap.wrap("  Your firing preference is " + pref + ".", 26)
    
    return (str(pref))


class BasicShot:
    def __init__(self, damage):
        self.damage = damage
    
    def hit(self, shooter, target, constants):
    
        results = []

        damage = self.damage - target.fighter.defense
        if target.name == 'Player':
            damage = int(damage * (constants['options_enemy_damage_scale']/100))
        else:
            damage = int(damage * (constants['options_player_damage_scale']/100))
            
        if damage > 0:
            results.append({'message': Message('{0} shoots {1} for {2} hit points.'.format(
                shooter.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} shoots {1} but does no damage.'.format(
                shooter.name.capitalize(), target.name), libtcod.white)})

        return results

class PoisonShot:
    def __init__(self, shot_damage, pos_damage, pos_duration):
        self.damage = shot_damage
        self.pos_damage = pos_damage
        self.pos_duration = pos_duration
        
    def hit(self, shooter, target, constants):
    
        results = []

        damage = self.damage - target.fighter.defense
        if target.name == 'Player':
            damage = int(damage * (constants['options_enemy_damage_scale']/100))
        else:
            damage = int(damage * (constants['options_player_damage_scale']/100))
            
        if damage > 0:
            results.append({'message': Message('{0} shoots {1} for {2} hit points.'.format(
                shooter.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
            
            poisoned = False
            for con in target.conditions:
                if con.name == "Poison":
                    #if already poisoned, set to active, reset duration and timer.
                    con.active = True
                    con.duration = self.pos_duration
                    con.timer = 1
                    poisoned = True
                    break
            if not poisoned: target.conditions.append(Poison(target, True, self.pos_duration, self.pos_damage))
                
            results.append({'message': Message('{0} is poisoned!'.format(
                target.name.capitalize()), libtcod.light_green)})
        else:
            results.append({'message': Message('{0} shoots {1} but does no damage.'.format(
                shooter.name.capitalize(), target.name), libtcod.white)})

        return results