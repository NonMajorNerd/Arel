import libtcodpy as libtcod
from game_messages import Message



class Poison:
    def __init__(self, target=None, active=True, duration=5, damage=2):
        
        self.char = "P"
        self.bgcolor = libtcod.Color(0, 255, 0)
        self.fgcolor = libtcod.Color(255, 0, 0)
        
        self.target = target
        self.active = active
        self.duration = duration
        self.timer = 1
        self.damage = damage        
    
    @property
    def tooltip(self):
        return ("Poison; Turn " + str(self.timer) + " of " + str(self.duration) + ".")
        

    def enact(self, **kwargs):
        results = []
        
        if self.timer < self.duration +1:
            if self.target.fighter:
                results.append({'damage': self.target.fighter.take_damage(self.damage)})
                if self.target.name == "Player":
                    results.append({ 'message': Message("You take " +  str(self.damage) + ' damage from poison.', libtcod.red)})
            else:
                print("Poision damage enacted on a non-fighter creature ... ")
            self.timer += 1
        else:
            self.target.conditions.remove(self)
            
        return results
        
class Healing:
    def __init__(self, target=None, active=True, duration=10, healing=1):
    
        self.char = "H"
        self.bgcolor = libtcod.Color(255, 255, 0)
        self.fgcolor = libtcod.Color(0, 0, 0)
    
        self.target = target
        self.active = active
        self.duration = duration

        self.timer = 1
        self.healing = healing

    @property
    def tooltip(self):
        return ("Healing; Turn " + str(self.timer) + " of " + str(self.duration) + ".")
        
    def enact(self, **kwargs):
        results = []
        
        if self.timer < self.duration +1:
            if self.target.fighter:
                self.target.fighter.heal(self.healing)
                if self.target.name == "Player":
                    results.append({ 'message': Message("you heal " + str(self.healing) + ' damage.', libtcod.green)})
            else:
                print("Healing enacted on a non-fighter creature ... ")
            self.timer += 1
        else:
            self.target.conditions.remove(self)
            
        return results
        
        