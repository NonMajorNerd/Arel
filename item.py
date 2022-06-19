import textwrap

class Item:
    def __init__(self, name=None, use_function=None, targeting=False, targeting_message=None, stackable=False, count=1, vendor_count=1,
        description="No Description", effect=None, flammable=False, ammo=None, range=0, cost=0, take_at_buy=True, **kwargs):
        
        self.name = name

        self.use_function = use_function                #what, if any, is this items "use" function?
        self.targeting = targeting                      #does this item require targeting when used?
        self.targeting_message = targeting_message      #what is the message displayed when targeting occurs
        
        self.stackable = stackable                      #is this item stackable?
        self.count = count                              #how many of this item are in this specific 'stack'?
        
        self.flammable = flammable                      #is this item flammable?
        
        self.ammo = ammo
        self.range = range

        self.cost = cost                                #how much does this item cost?
        self.take_at_buy = take_at_buy                  #is this item removed from the vendor's inventory upon player purchase?
        self.vendor_count = vendor_count                #used to differentiate how much of an item the vendor has versus the player
        
        self.description_lines = textwrap.wrap("  " + description, 26)               #description for display in the inventory system
        if len(self.description_lines) > 8:
            for line in self.description_lines:
                    print(str(line))
            raise Exception("Item description text is too long. Description text must wrap to 8 lines or fewer at 26 characters per line to fit in the inventory design.")
        
        self.effect_lines = None
        if effect: 
            self.effect_lines = textwrap.wrap("  " + effect, 26)                        #effect text for display in the inventory system
            if len(self.effect_lines) > 3:
                for line in self.effect_lines:
                    print(str(line))
                raise Exception("Item effect text is too long. Effect text must wrap to 3 lines or fewer at 26 characters per line to fit in the inventory design.")
        
        self.function_kwargs = kwargs
