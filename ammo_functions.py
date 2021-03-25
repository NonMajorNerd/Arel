import libtcodpy as libtcod
from game_messages import Message
from condition_functions import Poison

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