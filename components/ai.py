import libtcodpy as libtcod

from random import randint

from game_messages import Message
from components.fighter import Fighter
from entity import Entity
from render_functions import RenderOrder

class CameraMan:
    def take_turn(self, target, fov_map, game_map, entities, constants):
        results = []
        monster = self.owner

        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if int(monster.distance_to(target)) <= 3:
                monster.move_from(target, game_map, fov_map, entities)
               
            elif int(monster.distance_to(target)) > 5:
                monster.move_astar(target, entities, game_map)
               
            else:
                random_x = randint(-1, 1)
                random_y = randint(-1, 1)
                    
                ent_in_way = False
                for ent in entities:
                    if ent.x == monster.x+random_x and ent.y == monster.y+random_y and ent.blocks:
                        ent_in_way = True
                            
                if not ent_in_way and not game_map.tiles[monster.x+random_x][monster.y+random_y].block_sight:
                        if libtcod.map_is_in_fov(fov_map, monster.x+random_x, monster.y+random_y):
                            monster.move(random_x, random_y)
        else:
            monster.move_astar(target, entities, game_map)
            
        return results

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities, constants):
        results = []

        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target, constants)
                results.extend(attack_results)

        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities, constants):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return 
        
class RandomWalk:
    def __init__(self, randomfactor=50):
        self.randomfactor = randomfactor

    def take_turn(self, target, fov_map, game_map, entities, constants):
        results = []
        monster = self.owner
        
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            chance = randint(0, 100) 
            if chance <= self.randomfactor:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
            else:
                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target, constants)
                    results.extend(attack_results)

        return results

class RatKing:
    def __init__(self, randomfactor=50, ratchanceperturn=20, princechanceperturn=30):
        self.randomfactor = randomfactor
        self.ratchanceperturn = ratchanceperturn
        self.princechanceperturn =  princechanceperturn
        
    def take_turn(self, target, fov_map, game_map, entities, constants):
        results = []
        monster = self.owner
        
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            chance = randint(0, 100) 
            if chance <= self.randomfactor:
                random_x = self.owner.x + randint(0, 2) - 1
                random_y = self.owner.y + randint(0, 2) - 1

                if random_x != self.owner.x and random_y != self.owner.y:
                    self.owner.move_towards(random_x, random_y, game_map, entities)
            else:
                if monster.distance_to(target) >= 2:
                    monster.move_astar(target, entities, game_map)
                elif target.fighter.hp > 0:
                    attack_results = monster.fighter.attack(target, constants)
                    results.extend(attack_results)

        dice = randint(0, 100)
            
        if dice < self.ratchanceperturn:
            fighter_component = Fighter(hp=5, defense=0, power=3, speed=10, xp=5)
            ai_component = BasicMonster()
            spot_blocked = True
            while spot_blocked:
                x = self.owner.x + randint(1,5)
                y = self.owner.y + randint(1,5)
                if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                    if not x > game_map.width or y > game_map.height or game_map.tiles[x][y].block_sight or game_map.tiles[x][y].empty_space:
                        spot_blocked = False
            monster = Entity(x, y, 304, libtcod.Color(191, 191, 191), 'rat', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            entities.append(monster)
            
        elif dice < self.ratchanceperturn + self.princechanceperturn  + 1:
            fighter_component = Fighter(hp=5, defense=0, power=3, speed=10, xp=15)
            ai_component = BasicMonster()
            spot_blocked = True
            while spot_blocked:
                x = self.owner.x + randint(1,5)
                y = self.owner.y + randint(1,5)
                if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                    if not x > game_map.width or y > game_map.height or game_map.tiles[x][y].block_sight or game_map.tiles[x][y].empty_space:
                        spot_blocked = False
            monster = Entity(x, y, 330, libtcod.lighter_violet, 'rat prince', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
            entities.append(monster)

        return results