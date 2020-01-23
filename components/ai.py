import libtcodpy as libtcod

from random import randint

from game_messages import Message


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
