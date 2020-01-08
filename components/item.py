class Item:
    def __init__(self, use_function=None, targeting=False, targeting_message=None, stackable=False, count=1, **kwargs):
        self.use_function = use_function            #what, if any, is this items use function?
        self.targeting = targeting                      #does this item require targeting when used?
        self.targeting_message = targeting_message          #what is the message displayed when targeting occurs
        
        self.stackable = stackable                  #is this item stackable?
        self.count = count                              #how many of this item are in this 'stack'?
        self.function_kwargs = kwargs
