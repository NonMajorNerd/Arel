import libtcodpy as libtcod

from game_messages import Message
from entity import get_ent_name


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

    def add_item(self, item, names_list):
        results = []

        stacked = False
        for i in self.items:
            if i.name == item.name and i.item.stackable:
                i.item.count += 1
                stacked = True
                name = get_ent_name(item, names_list)
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
                name = get_ent_name(item, names_list)
                results.append({
                    'item_added': item,
                    'message': Message('You pick up the {0}!'.format(name), libtcod.blue)
                })

            self.items.append(item)

        return results

    def use(self, item_entity, names_list, colors_list, **kwargs):
        results = []
        used = False
        
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

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)
                used = True
                results.extend(item_use_results)

        #if the item was used, it is automatically identified. Update the 'names_list' with the real name of the item.
        if used:
            colors_list[item_entity.name] = colors_list[names_list[item_entity.name]]       #add a new key for the indentified name (eg 'Healing Potion') using the unidentified names current value (eg 'Cyan Potion')
            del colors_list[names_list[item_entity.name]]                                   #remove the unidentified names value (eg 'Cyan Potion')
            names_list[item_entity.name] = item_entity.name                                 #update the name in the names list

        return results

    def remove_item(self, item):
        if item.item.stackable:
            if item.item.count > 1:
                item.item.count -=1
            else:
                self.items.remove(item)
        else:
            self.items.remove(item)


    def drop_item(self, item):
        results = []

        #TODO :: Add other equipment slots..
        if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y
        
        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 libtcod.yellow)})

        return results
