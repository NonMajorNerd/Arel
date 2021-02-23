import textwrap

class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, stackable=False, count=1,
        description="No Description", effect=None, flammable=False, **kwargs):
        
        self.use_function = use_function            #what, if any, is this items "use" function?
        self.targeting = targeting                      #does this item require targeting when used?
        self.targeting_message = targeting_message          #what is the message displayed when targeting occurs
        
        self.stackable = stackable                  #is this item stackable?
        self.count = count                              #how many of this item are in this specific 'stack'?
        
        self.flammable = flammable                    #is this item flammable?
        
        self.description_lines = textwrap.wrap("  " + description, 26)               #description for display in the inventory system
        if len(self.description_lines) > 8:
            for line in self.description_lines:
                    print(str(line))
            raise Exception("Item description is too long. Description text must wrap (26 characters) to 8 lines or less to fit in the inventory design.")
        
        self.effect_lines = None
        if effect: 
            self.effect_lines = textwrap.wrap("  " + effect, 26)                        #effect text for display in the inventory system
            if len(self.effect_lines) > 3:
                for line in self.effect_lines:
                    print(str(line))
                raise Exception("Item effect text is too long. Effect text must wrap (26 characters) to 3 lines or less to fit in the inventory design.")
        
        self.function_kwargs = kwargs
