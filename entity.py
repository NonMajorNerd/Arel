import libtcodpy as libtcod

import math

from components.item import Item
from render_functions import RenderOrder

import random

def get_ent_name(ent, names_list):
    return names_list[ent.name]

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x, y, char, color, name, blocks=False,
        render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None,
        level=None, equipment=None, equippable=None, ammo=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable
        self.ammo = ammo
        self.conditions = []

        if self.name == "Player":
            self.character_name = "Player"
            
            self.kill_counts = []
            self.turn_count = 0
            self.score = 0
            
            #achievements
            self.potions_drank = 0
            self.scrolls_read = 0
            self.gold_collected = 0


        if self.fighter: self.fighter.owner = self
        if self.ai: self.ai.owner = self
        if self.item: self.item.owner = self
        if self.inventory: self.inventory.owner = self
        if self.stairs: self.stairs.owner = self
        if self.level: self.level.owner = self
        if self.equipment: self.equipment.owner = self
        
        if self.equippable: 
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self
        
        if self.conditions: self.conditions.owner = self

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                    get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

            
    def move_from(self, target, game_map, fov_map, entities):

        dx = target.x - self.x
        dy = target.y - self.y

        mx = []
        my = []
        
        moves =[]

        if dx > 0: #i need to move left
            mx.append(-1)
            mx.append(0)
            
        elif dx < 0: #i need to move right
            mx.append(1)
            mx.append(0)
        else:
            mx.append(1)
            mx.append(-1)
            mx.append(0)
            
        if dy > 0: #i need to move down
            my.append(-1)
            my.append(0)
        elif dy < 0: #i need to move up
            my.append(1)
            my.append(0)
        else:
            my.append(-1)
            my.append(1)
            my.append(0)
            
        for x in mx:
            for y in my:
                if not (x, y) == (0, 0):
                    ent_in_way = False
                    for ent in entities:
                        if ent.x == self.x+x and ent.y == self.y+y: #if you add and. ent.blocks: then we will only avoid other actors..
                            if not ent.name == "Junk" and ent.blocks:              #excluding this means we avoid all entities other than Junk
                                ent_in_way = True                   
                            
                    if not ent_in_way and not game_map.tiles[self.x+x][self.y+y].block_sight:
                        if libtcod.map_is_in_fov(fov_map, self.x+x, self.y+y):
                            moves.append ([x, y])

        if not len(moves) == 0:    
            choice = random.randint(0, len(moves)-1)
            
            (nx, ny) = moves[choice]
            self.x += nx
            self.y += ny
        
    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, target, entities, game_map):
        # Create a FOV map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        # Compute the path between self's coordinates and the target's coordinates
        libtcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # Delete the path to free memory
        libtcod.path_delete(my_path)


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
