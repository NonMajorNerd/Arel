from components.ammo import Ammo
import libtcodpy as libtcod
from game_messages import Message
from condition_functions import Poison
from menus import m1m2_menu

def Fire_And_Preference(called_from=None, player=None, constants=None):
    if not called_from: print("Error; ammo_functions line 7.. F&P without called from")
    if not constants: print("Error; ammo_functions line 7.. F&P without constants")
    
    ammo_list =[]

    for i in player.inventory.items:
        print(str(i.name))
        if i.item.ammo:
            ammo_list.append(i.name)

    print(str(ammo_list))

    if len(ammo_list) == 0:
        print("no ammo")
        return None

    pref = constants['options_ammo_preference']
    print('pref: ' + str(pref))

    if called_from == "Map":

        if pref == None:

            numoptions = 4

            #find the longest string in options list to define menu width
            max_len = -1
            for opt in ammo_list:
                if len(opt) > max_len:
                    max_len = len(opt)

            w = max_len + 5
            if w < 15: w = 15

            h = numoptions + 2

            x = player.x + 1
            y = player.y - (h+1)

            if x + w >= constants['screen_width'] -1:
                x -= (w+1)

            while y <= 1:
                y += 1

            pref = m1m2_menu(x, y, w, h, numoptions, ammo_list)

        constants['options_ammo_preference'] = pref
        return (str(pref))

    elif called_from == "Inventory":
        return 4
        #presuming the quiver is calling this..
        #the arrow/ammo will use its entity.item "Use_Function()" to assign/overwrite preference

        #preference = m1()

    else:
        print("huh?")



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