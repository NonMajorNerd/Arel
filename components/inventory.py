import libtcodpy as libtcod
import textwrap
import _globals

from game_messages import Message
from entity import get_ent_name
from ammo_functions import m1m2_menu

class Inventory:
    def __init__(self, capacity):
        self.base_capacity = capacity
        self.items = []

    @property
    def max_capacity(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.capacity_bonus
        else:
            bonus = 0

        return self.base_capacity + bonus

    def add_item(self, item, quantity): 
        results = []

        stacked = False
        for i in self.items:
            if i.name == item.name and i.item.stackable:
                i.item.count += quantity
                stacked = True
                name = get_ent_name(item, _globals.names_list)
                results.append({
                    'item_added': item,
                    'message': Message('You pick up the {0}!'.format(name), libtcod.blue)
                })
                
        if not stacked:
            if len(self.items) >= self.max_capacity:
                results.append({
                    'item_added': None,
                    'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
                })
            else: 
                name = _globals.get_from_dict(_globals.names_list, item)
                results.append({
                    'item_added': item,
                    'message': Message('You pick up the {0}!'.format(name), libtcod.blue)
                })

            if item.name == 'Gold': #don't add a physical 'Gold" item, just increase the player's current_gold & gold_collected values
                self.owner.gold_collected += quantity; self.owner.current_gold += quantity 
            else:
                self.items.append(item)
                for i in range(quantity):
                    self.items.append(item) 

        return results

    def use(self, item_entity, **kwargs):
        results = []
        used = False
            
        #special-case handling for the quiver 'item'
        if True:
            if item_entity.name == 'Quiver':
                ammo_list = []

                for i in self.items:
                    if i.item.ammo:
                        ammo_list.append(i.name)

                if len(ammo_list) == 0:
                    results.append({'message': Message('You do not have any ammo to select with your quiver.', libtcod.light_red)})
                    return results
                    
                pref = m1m2_menu(x=31, y=21, w=25, h=8, numoptions=8, optionslist=ammo_list)

                _globals.constants['options_ammo_preference'] = pref

                if pref == None:
                    item_entity.item.effect_lines = textwrap.wrap("  Firing preference is currently unassigned.", 26) 
                else:
                    item_entity.item.effect_lines = textwrap.wrap("  Your firing preference is " + pref + ".", 26)
                    results.append({'message': Message('You have updated your default ammo preference.', libtcod.light_gray)})

                return results
                
        item_component = item_entity.item
        
        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                used = True
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name), libtcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)
                if item_use_results:
                    for item_use_result in item_use_results:
                        if item_use_result.get('consumed'):
                            self.remove_item(item_entity)
                    used = True
                
                    results.extend(item_use_results)

        #if the item was used, it is automatically identified. Update the 'names_list' with the real name of the item.
        if used:
            if not item_entity.name in _globals.colors_list.keys():
                if _globals.names_list[item_entity.name] in _globals.colors_list.keys():
                    _globals.colors_list[item_entity.name] = _globals.colors_list[_globals.names_list[item_entity.name]]       #add a new key for the indentified name (eg 'Healing Potion') using the unidentified names current value (eg 'Cyan Potion')
                    del _globals.colors_list[_globals.names_list[item_entity.name]]                                   #remove the unidentified names value (eg 'Cyan Potion')
            _globals.names_list[item_entity.name] = item_entity.name                                         #update the name in the names list

        return results

    def remove_item(self, item):
        if item.item.stackable and item.item.count > 1:
                item.item.count = item.item.count - 1
        else:       
            self.items.remove(item)


    def drop_item(self, item):
        results = []

        if item.name == 'Gold':
            results.append({'message': Message("You can't drop your gold!", libtcod.yellow)})
        else:
            #TODO :: Add other equipment slots..
            if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
                self.owner.equipment.toggle_equip(item)

            item.x = self.owner.x
            item.y = self.owner.y
            
            self.remove_item(item)
            results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                     libtcod.yellow)})

        return results
