class Equippable:
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, speed_bonus=0, luck_bonus=0, capacity_bonus=0, **kwargs):
        self.slot = slot
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.speed_bonus = speed_bonus
        self.luck_bonus = luck_bonus
        self.capacity_bonus = capacity_bonus