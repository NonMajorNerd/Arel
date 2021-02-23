from equipment_slots import EquipmentSlots

## TODO :: 
    # Build support for two-handed weapons
    # Replace ACC1 and ACC2 with a single system that can support up to two accessories

class Equipment:
    def __init__(self, main_hand=None, off_hand=None, helm=None, armor=None, accessory1=None, accessory2=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.helm = helm
        self.armor = armor
        self.accessory1 = accessory1
        self.accessory2 = accessory2
 
    @property
    def list(self):
        return [self.main_hand, self.off_hand, self.helm, self.armor, self.accessory1, self.accessory2]
        
    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.max_hp_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.max_hp_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.max_hp_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.power_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.power_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.power_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.power_bonus

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defense_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defense_bonus

        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.defense_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.defense_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.defense_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.defense_bonus

        return bonus

    @property
    def speed_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.speed_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.speed_bonus

        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.speed_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.speed_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.speed_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.speed_bonus

        return bonus
        
    @property
    def luck_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.luck_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.luck_bonus

        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.luck_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.luck_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.luck_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.luck_bonus

        return bonus
        
    @property
    def capacity_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.capacity_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.capacity_bonus
            
        if self.helm and self.helm.equippable:
            bonus += self.helm.equippable.capacity_bonus

        if self.armor and self.armor.equippable:
            bonus += self.armor.equippable.capacity_bonus
            
        if self.accessory1 and self.accessory1.equippable:
            bonus += self.accessory1.equippable.capacity_bonus
            
        if self.accessory2 and self.accessory2.equippable:
            bonus += self.accessory2.equippable.capacity_bonus

        return bonus


    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand: results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
                
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand: results.append({'dequipped': self.main_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})
                
        elif slot == EquipmentSlots.HELM:
            if self.helm == equippable_entity:
                self.helm = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.helm:
                    results.append({'dequipped': equippable_entity})
                    
                self.helm = equippable_entity
                results.append({'equipped': equippable_entity})
        
        elif slot == EquipmentSlots.ARMOR:
            if self.armor == equippable_entity:
                self.armor = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.armor:
                    results.append({'dequipped': equippable_entity})
                    
                self.armor = equippable_entity
                results.append({'equipped': equippable_entity})
        
        elif slot == EquipmentSlots.ACC1:
            if self.accessory1 == equippable_entity:
                self.accessory1 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.accessory1:
                    results.append({'dequipped': equippable_entity})
                    
                self.accessory1 = equippable_entity
                results.append({'equipped': equippable_entity})
        
        elif slot == EquipmentSlots.ACC2:
            if self.accessory2 == equippable_entity:
                self.accessory2 = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.accessory2:
                    results.append({'dequipped': equippable_entity})
                    
                self.accessory2 = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
