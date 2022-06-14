import libtcodpy as libtcod

from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power, speed=5, luck=0, xp=0, gold=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.base_speed = speed
        self.timer = 0
        self.base_luck = luck
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus
    
    @property
    def speed(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.speed_bonus
        else:
            bonus = 0

        return self.base_speed + bonus
        
    @property
    def luck(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.luck_bonus
        else:
            bonus = 0

        return self.base_luck + bonus

    @property
    def gold(self):
        
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.luck_bonus
        else:
            bonus = 0
            
        return self.gold + bonus
      
    def take_damage(self, amount):
        results = []

        self.hp -= amount
        print (self.owner.name + 'took ' + str(amount) + ' damage.')
        if self.hp <= 0:
            self.hp = 0
            results.append({'dead': self.owner, 'xp': self.xp})
        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target, constants):
        results = []

        damage = self.power - target.fighter.defense
        if target.name == 'Player':
            damage = int(damage * (constants['options_enemy_damage_scale']/100))
        else:
            damage = int(damage * (constants['options_player_damage_scale']/100))
            
        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})

        return results

