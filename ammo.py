class Ammo:
    def __init__(self, hit_function=None, retrievable=False, **kwargs):
        
        self.hit_function = hit_function
        self.retrievable = retrievable