import tcod as libtcod
from random import randint, choice

from components.ai import BasicMonster, RandomWalk, CameraMan
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs

from entity import Entity

from game_messages import Message

from item_functions import cast_confuse, cast_fireball, cast_lightning, heal

from map_objects.rectangle import Rect
from map_objects.tile import Tile, Door

from random_utils import from_dungeon_level, random_choice_from_dict

from render_functions import RenderOrder


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level
        
        self.door_tiles = []

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, names_list, render_colors_list):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)
            # random position without going out of the boundaries of the map (with a 1-tile buffer as well)
            x = randint(1, map_width - w - 2)
            y = randint(1, map_height - h - 2)

            # "Rect" class makes rectangles easier to work with
            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
            else:
                # this means there are no intersections, so this room is valid

                # "paint" it to the map's tiles
                self.create_room(new_room)

                # center coordinates of new room, will be useful later
                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # this is the first room, where the player starts at
                    player.x = new_x
                    player.y = new_y
                    

                    
                else:
                    # all rooms after the first:
                    # connect it to the previous room with a tunnel

                    # center coordinates of previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin (random number that is either 0 or 1)
                    if randint(0, 1) == 1:
                        # first move horizontally, then vertically
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        # first move vertically, then horizontally
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, names_list, render_colors_list)
                self.place_junk(new_room, entities)
                    
                # finally, append the new room to the list
                rooms.append(new_room)
                num_rooms += 1

        self.clean_map()
    
        self.assign_blitmap()

        self.create_doors()

        #make the first camera man!!!
        fighter_component = Fighter(hp=15, defense=0, power=0, speed=5)
        ai_component = CameraMan()
        w = int(rooms[len(rooms)-1].w / 2) 
        h = int(rooms[len(rooms)-1].h / 2)
        spot_blocked = True
        while spot_blocked:
            rx = randint(-w, w)
            ry = randint(-h, h)
            if not any([entity for entity in entities if entity.x == player.x+rx and entity.y == player.y+ry]):
                if not self.tiles[player.x + rx][player.y + ry].block_sight or self.tiles[player.x+rx][player.y+ry].empty_space:
                    spot_blocked = False
        
        cameraman = Entity(player.x +rx, player.y +ry, 301, libtcod.Color(191, 191, 191), 'Camera Op.', blocks=True, render_order=RenderOrder.ACTOR,
                        fighter=fighter_component, ai=ai_component)
        entities.append(cameraman)  
        
        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, 320, (102,102,153), 'Stairs',
                             render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)        

    def clean_map(self):
        #this iterates through the map and turns unused wall space into empty space so that the autotile function will work in rendering
        
        locations = []
        
        #for every tile in the map..
        for y in range (self.height ):
            for x in range (self.width):
                
                #assume it IS surrounded
                allwalls = True
                
                #check all adjacent tiles
                for dy in range (-1, 2):
                    for dx in range (-1, 2):

                        #as long as they are in range (not outside the map/screen)
                        if y + dy >= 0 and y + dy <= self.height-1:
                            if x + dx >= 0 and x + dx <= self.width-1:
                                
                                #if any of the tiles in question are a floor,
                                if self.tiles[x+dx][y+dy].block_sight == False:
                                
                                    #then this tile is not surrounded
                                    allwalls = False
                            
                #if (after checking all adjacent tiles) this tile is surrounded,   
                if allwalls == True:
                    #add this location to the list to be changed    
                    locations.append ((x, y))

        #change all locations
        for (x, y) in locations:
            self.tiles[x][y] = Tile(False)
            self.tiles[x][y].empty_space = True
            
    def is_wall(self, x, y):
        if y >= 0 and y <= self.height:
            if x >= 0 and x <= self.width:
                return self.tiles[x][y].block_sight
            
        return False

    def is_empty(self, x, y):
        if y >= 0 and y <= self.height:
            if x >= 0 and x <= self.width:
                return self.tiles[x][y].empty_space
            
        return False

    def assign_blitmap(self):
    
        self.blitmap = [[99 for y in range(self.height)] for x in range(self.width)]
   
        # Draw all the tiles in the game map
        for y in range(self.height -1):
            for x in range(self.width -1):
               
               # [   ] [ 1 ] [   ]
               # [ 8 ] [ 0 ] [ 2 ]
               # [   ] [ 4 ] [   ]

                if self.is_wall(x, y):
                    
                    iBlit = 0
                    
                    if self.is_wall(x, y-1): iBlit += 1
                    if self.is_wall(x+1, y): iBlit += 2
                    if self.is_wall(x, y+1): iBlit += 4
                    if self.is_wall(x-1, y): iBlit += 8
               
                    #print(str(iBlit))
                    
                    self.blitmap[x][y] = iBlit
                
    def create_doors(self):
        print ('making doors again')
        self.door_tiles = []
    
        for y in range(self.height-1):
            for x in range(self.width-1):
            
                if not self.is_wall(x,y):
                    if self.is_wall(x, y-1) and self.is_wall(x, y+1):
                        #check all tiles to the left and right
                        if ((not self.is_wall(x-1, y-1) and not self.is_wall(x-1, y) and not self.is_wall(x-1, y+1)) and
                            (not self.is_empty(x-1, y-1) and not self.is_empty(x-1, y) and not self.is_empty(x-1, y+1))):
                            
                            other_doors = False
                            
                            for oy in range (-3, 4):
                                for ox in range (-3, 4):
                                    for (sx, sy) in self.door_tiles:
                                        if sx == x + ox and sy == y + oy:
                                            other_doors = True
                               
                            if not other_doors:
                                self.door_tiles.append((x,y))
                                
                        if ((not self.is_wall(x+1, y-1) and not self.is_wall(x+1, y) and not self.is_wall(x+1, y+1)) and
                            (not self.is_empty(x+1, y-1) and not self.is_empty(x+1, y) and not self.is_empty(x+1, y+1))):
                            
                            other_doors = False
                            
                            for oy in range (-3, 4):
                                for ox in range (-3, 4):
                                    for (sx, sy) in self.door_tiles:
                                        if sx == x + ox and sy == y + oy:
                                            other_doors = True
                               
                            if not other_doors:
                                self.door_tiles.append((x,y))
                            
                    if self.is_wall(x-1, y) and self.is_wall(x+1, y):
                        #check all tiles above and below
                        if ((not self.is_wall(x-1, y-1) and not self.is_wall(x, y-1) and not self.is_wall(x+1, y-1)) and
                            (not self.is_empty(x-1, y-1) and not self.is_empty(x, y-1) and not self.is_empty(x+1, y-1))):
                            
                            other_doors = False
                            
                            for oy in range (-3, 4):
                                for ox in range (-3, 4):
                                    for (sx, sy) in self.door_tiles:
                                        if sx == x + ox and sy == y + oy:
                                            other_doors = True
                               
                            if not other_doors:
                                self.door_tiles.append((x,y))
                                
                        if ((not self.is_wall(x-1, y+1) and not self.is_wall(x, y+1) and not self.is_wall(x+1, y+1)) and
                            (not self.is_empty(x-1, y+1) and not self.is_empty(x, y+1) and not self.is_empty(x+1, y+1))):
                            
                            other_doors = False
                            
                            for oy in range (-3, 4):
                                for ox in range (-3, 4):
                                    for (sx, sy) in self.door_tiles:
                                        if sx == x + ox and sy == y + oy:
                                            other_doors = True
                               
                            if not other_doors:
                                self.door_tiles.append((x,y))
                                
                                
                    
        for (x,y) in self.door_tiles:
            
            open_chance = randint(1, 5)
            open = False
            if open_chance == 1:
                open = True
                
            door_component = Door(is_open=open, is_locked=False, keys=[])
            self.tiles[x][y].door = door_component
                
            self.tiles[x][y].block_sight = not open
            self.tiles[x][y].blocked = not open                  

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_junk(self, room, entities):
    
        # Get a random number of junk items    
        number_of_junks = randint(-1, 2) + 1
        
        # Get a random type of junk
        junk_symbol = randint(0, 3)
        
        if junk_symbol == 0:
            junk_char = 249
        elif junk_symbol == 1:
            junk_char = 250
        else:
            junk_char = 255
        
        for i in range(number_of_junks):
            # Choose a random location in the room
            x = randint(room.x1 + 2, room.x2 - 2)
            y = randint(room.y1 + 2, room.y2 - 2)
            
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                new_junk = Entity(x, y, junk_char, (51,51,102), 'Junk', render_order=RenderOrder.JUNK, blocks=False)
                entities.append(new_junk)
            
    def place_entities(self, room, entities, names_list, render_colors_list):
        max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level([[1, 1], [2, 4]], self.dungeon_level)
        
        # Get a random number of monsters
        number_of_monsters = randint(0, max_monsters_per_room)
        
        # Get a random number of items
        number_of_items = randint(1, max_items_per_room)

        monster_chances = {
            'rat': from_dungeon_level([[40, 1], [30, 2], [25, 3]], self.dungeon_level),
            'bat': 50,
            'goblin': 30,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level)
        }

        item_chances = {
            #HEALING POT TEST
            #'healing_potion': 100,
            
            #SCROLL TEST
            #'healing_potion': 25,
            #'lightning_scroll': 25,
            #'fireball_scroll': 25,
            #'confusion_scroll': 25
            
            'healing_potion': 15,
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2], [15, 3], [20,4]], self.dungeon_level)
        }

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            # Check if an entity is already in that location
            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'rat':
                    fighter_component = Fighter(hp=5, defense=0, power=3, speed=10, xp=15)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 304, libtcod.Color(191, 191, 191), 'rat', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                                
                    chance_for_swarm = 60
                    swarm_check = randint(0, 100)
                    if swarm_check >= chance_for_swarm:
                        for i in range(1, randint(0,4)+1):
                            rx = randint(room.x1 + 1, room.x2 - 1)
                            ry = randint(room.y1 + 1, room.y2 - 1)
                            if not any([entity for entity in entities if entity.x == rx and entity.y == ry]):
                                fighter_component = Fighter(hp=5, defense=0, power=3, speed=8, xp=15)
                                ai_component = BasicMonster()
                                monster = Entity(rx, ry, 304, libtcod.Color(191, 191, 191), 'rat', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                                entities.append(monster)

                elif monster_choice == 'bat':
                    fighter_component = Fighter(hp=10, defense=0, power=3, speed=10, xp=15)
                    ai_component = RandomWalk(randomfactor=66)

                    monster = Entity(x, y, 305, libtcod.Color(191, 191, 191), 'bat', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)
                    
                elif monster_choice == 'goblin':
                    fighter_component = Fighter(hp=20, defense=0, power=4, speed=5, xp=35)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 295, libtcod.Color(107, 164, 107), 'goblin', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                else: #troll
                    fighter_component = Fighter(hp=30, defense=2, power=8, speed=5, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 296, libtcod.Color(242, 221, 131), 'troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)


                entities.append(monster)

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, stackable=False, amount=40,
                        description="A small glass vial containing a semi-translusent crystalline liquid which shimmers slightly in the light.",
                        effect="Typically used to cure minor wounds.")
                    #item = Entity(x, y, 349, render_colors_list[names_list['Healing Potion']], 'Healing Potion',  identified=False, render_order=RenderOrder.ITEM,
                    #              item=item_component)
                    item = Entity(x, y, 349, render_colors_list[names_list['Healing Potion']], 'Healing Potion', render_order=RenderOrder.ITEM,
                                  item=item_component)
                elif item_choice == 'sword':
                    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, 369, libtcod.sky, 'Sword', equippable=equippable_component)
                    
                elif item_choice == 'shield':
                    equippable_component = Equippable(EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, 375, libtcod.darker_orange, 'Shield', equippable=equippable_component)
                    
                elif item_choice == 'fireball_scroll':
                    item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                        'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                          damage=25, radius=3, flammable=False)  #Fireball scrolls are not flamable
                    item = Entity(x, y, 333, choice(render_colors_list['Scrolls']), 'Fireball Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                                  
                elif item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan), flammable=True)
                    item = Entity(x, y, 333, choice(render_colors_list['Scrolls']), 'Confusion Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)
                                  
                else:
                    item_component = Item(use_function=cast_lightning, damage=40, maximum_range=5, flammable=True)
                    item = Entity(x, y, 333, choice(render_colors_list['Scrolls']), 'Lightning Scroll', render_order=RenderOrder.ITEM,
                                  item=item_component)

                entities.append(item)

                    

    def is_blocked(self, x, y):
        return self.tiles[x][y].blocked


    def next_floor(self, player, message_log, constants, names_list, render_colors_list):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, names_list, render_colors_list)

        player.fighter.heal(player.fighter.max_hp // 2)

        message_log.add_message(Message('You take a moment to rest, and recover your strength.', libtcod.light_violet))

        return entities
