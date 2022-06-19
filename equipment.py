from equipment_slots import EquipmentSlots

## TODO :: 
    # Build support for two-handed weapons
    # Replace ACC1 and ACC2 with a single system that can support up to two accessories

def StatChange(equipment, item):
    #equipment is an Equipment component, item is an Equippable component
                
    # This function will return a dictionary of stat changes based on the equipment and
    # the item (equipment) passed to it. 
    
    results = {}
        
    if not item.slot:
        raise Exception("Item to compare is a non-equippable component. Pass only the equippable component of the item to this function.")
        
    if (item.slot == EquipmentSlots.MAIN_HAND and item.owner.name == equipment.main_hand.name) or (item.slot == EquipmentSlots.OFF_HAND and item.owner.name == equipment.off_hand.name) or (item.slot == EquipmentSlots.HELM and item.owner.name == equipment.off_hand.name) or (item.slot == EquipmentSlots.ARMOR and item.owner.name == equipment.off_hand.name) or (item.slot == EquipmentSlots.ACC1 and item.owner.name == equipment.off_hand.name) or (item.slot == EquipmentSlots.ACC2 and item.owner.name == equipment.off_hand.name):
        return results  
    else:
        x = 1
        
        return results

class Equipment:
    def __init__(self):
        self.list = []
        
    @property
    def max_hp_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.max_hp_bonus
        return bonus

    @property
    def power_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.power_bonus
        return bonus

    @property
    def defense_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.defense_bonus
        return bonus

    @property
    def speed_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.speed_bonus
        return bonus
        
    @property
    def luck_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.luck_bonus
        return bonus
        
    @property
    def capacity_bonus(self):
        bonus = 0
        for e in self.list:
            if e.equippable:
                bonus += e.equippable.capacity_bonus
        return bonus

    def toggle_equip(self, equippable_entity):
        
        results = []
        
        if not equippable_entity.equippable:
            print(equippable_entity.name + " doesn't have an equippable component. [line 81 equipment.py]")
            return results

        if equippable_entity in self.list:
            self.list.remove(equippable_entity)
            results.append({'dequipped': equippable_entity})
            return results
                      
        slot = equippable_entity.equippable.slot
        
        for e in self.list:
            if e.equippable.slot == equippable_entity.equippable.slot:
                self.list.remove(e)
                results.append({'dequipped': e})
                self.list.append(equippable_entity)
                results.append({'equipped': equippable_entity})  
                return results
        
        self.list.append(equippable_entity)
        results.append({'equipped': equippable_entity})  
        return results