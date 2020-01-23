import libtcodpy as libtcod

from game_messages import Message

class Poison:
    def __init__(self, target=None, active=True, duration=5, damage=2):
        self.target = target
        self.active = active
        self.duration = duration
        self.timer = 1
        self.damage = damage        

    def inact(self):
        results = []
        
        if self.timer < self.duration +1:
            print ('Poison turn ' + str(self.timer) + ' of ' + str(self.duration))
            if self.target.fighter: self.target.fighter.take_damage(self.damage)
            results.append({ 'message': Message('You take ' + str(self.damage) + ' damage from poison.', libtcod.red)})

            self.timer += 1
            
        return results
        
class Healing:
    def __init__(self, target=None, active=True, duration=10, healing=1):
        self.target = target
        self.active = active
        self.duration = duration
        self.timer = 1
        self.healing = healing        

    def inact(self):
        results = []
        
        if self.timer < self.duration +1:
            print ('Healing turn ' + str(self.timer) + ' of ' + str(self.duration))
            if self.target.fighter: self.target.fighter.heal(self.healing)
            results.append({ 'message': Message('You heal ' + str(self.healing) + ' damage.', libtcod.green)})

            self.timer += 1
            
        return results