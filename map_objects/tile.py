class Tile:
    """
    A tile on a map. It may or may not be blocked, and may or may not block sight.
    """
    def __init__(self, blocked, block_sight=None, door=None):
        self.blocked = blocked
        self.door = door
        
        if self.door:
            self.block_sight = not self.door.is_open
        elif block_sight is None:
            self.block_sight = blocked
        else:
            self.block_sight = block_sight
        
        self.explored = False
        self.empty_space = False
        
        
class Door:
    
        def __init__(self, is_open=False, is_locked=False, keys=[]):
            self.is_open = is_open
            self.keys = keys
            
            if self.keys == []:
                self.is_locked = False
            else:
                self.is_locked = is_locked
            
            if self.is_open:
                self.char = 196
            else:
                self.char = 197
            
        def toggle_open(self, game_map, x, y):
            self.is_open = not self.is_open
            
            if self.is_open:
                self.char = 196
            else:
                self.char = 197
                
            game_map.tiles[x][y].block_sight = not self.is_open
            game_map.tiles[x][y].blocked = not self.is_open
             

   
            
            
            
            
