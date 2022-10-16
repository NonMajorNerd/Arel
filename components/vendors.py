import tcod as libtcod
import _globals
import _items
import shelve
import map_objects.game_map as game_map

from components.item import Item
from game_messages import Message
from menus import get_item_at, get_name_string

class vendor_data_loader:

    """
    A Set of functions for handling vendor data
    """

    def save_vendor_inventory():

        with shelve.open('data_files/vendor_data', 'c') as vendor_data:
            vendor_data['inventory_index'] = _globals.vendor_stock

    def load_vendor_inventory():
        with shelve.open('data_files/vendor_data', 'c') as vendor_data:
            vendor_stock = vendor_data['inventory_index']
        return vendor_stock

    def populate_vendor_inventory(): #watcha hawkin? (I'll figure out a better way to handle this later, for now it works for implementation n testing)
        
        #weapons
        _globals.vendorEnt.equipment.list.append(_items.staff)
        _globals.vendorEnt.equipment.list.append(_items.sword)
        _globals.vendorEnt.equipment.list.append(_items.dagger)
        _globals.vendorEnt.inventory.add_item(_items.bow, 1)
        _globals.vendorEnt.inventory.add_item(_items.quiver, 1)

        #consumables
        _globals.vendorEnt.inventory.add_item(_items.arrow, 100)
        _globals.vendorEnt.inventory.add_item(_items.psn_arrow, 10)

        #amor/accessories 
        _globals.vendorEnt.equipment.list.append(_items.shield) 
        _globals.vendorEnt.equipment.list.append(_items.fingerless_gloves)
        _globals.vendorEnt.equipment.list.append(_items.cargo_shorts)
        _globals.vendorEnt.equipment.list.append(_items.merchants_bag)
        
        _globals.vendor_stock = [_globals.vendorEnt.inventory.items, _globals.vendorEnt.equipment.list]

        return 

def vendor_menu(player):
    results = []
    
    #UI Color Defaults
    screen_yellow = libtcod.Color(255,255,102)
    screen_blue = libtcod.Color(102,178,255)
    screen_red = libtcod.Color(254,95,85)
    screen_green = libtcod.Color(178,255,102)
    screen_purple = libtcod.Color(102,46,155)
    screen_darkgray = libtcod.Color(102,102,102)    #background gray
    screen_midgray = libtcod.Color(158,158,158)     #dark lines gray    
    screen_lightgray = libtcod.Color(191,191,191)   #light lines gray, desc. text

    #Initial Inventory Variables
    index = 0
    itemsperpage = 24
    numitems = len(_globals.vendorEnt.inventory.items)
    numequip = len(_globals.vendorEnt.equipment.list) # - player.equipment.list.count('None')
    currentpage = 1
    # sort = _globals.constants['options_inventory_sort']
    # needs_sort = True
    
    #Make sure there is inventory to display
    if numitems + numequip == 0:
        results.append({'message': Message("Ya' cabbash", libtcod.white)})
        return results


    #print static UI elements
    if True:
        libtcod.console_set_default_background(0, libtcod.black)
        libtcod.console_clear(0)
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, libtcod.black)
    
        #backgrounds and border
        for y in range (2, 39):
            for x in range (1, 59):
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
                if y == 2 or y == 11 or y == 38:
                    libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
       
        for x in range(1, 12):
            libtcod.console_print_ex(0, x, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(205))
            
        for y in range(2, 39):
            libtcod.console_print_ex(0, 1, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
            libtcod.console_print_ex(0, 58, y, libtcod.BKGND_SET, libtcod.LEFT, chr(186))
        
        
        #corners, T pieces
        libtcod.console_print_ex(0, 1, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(201))
        libtcod.console_print_ex(0, 11, 1, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
        libtcod.console_print_ex(0, 11, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
        libtcod.console_print_ex(0, 58, 2, libtcod.BKGND_SET, libtcod.LEFT, chr(187))
        libtcod.console_print_ex(0, 1, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(199))
        libtcod.console_print_ex(0, 58, 11, libtcod.BKGND_SET, libtcod.LEFT, chr(182))
        libtcod.console_print_ex(0, 1, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(200))
        libtcod.console_print_ex(0, 58, 38, libtcod.BKGND_SET, libtcod.LEFT, chr(188))
      
        #stats, slots
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, libtcod.white)
            
        #dialogue from the vendor
        libtcod.console_print_ex(0, 6, 5, libtcod.BKGND_NONE, libtcod.LEFT, "Welcome, weary contestant, to my humble shop.")

        libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_NONE, libtcod.LEFT, "Please, browse at your lesiure; you are safe here.")

        libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "Well, as safe as you'll ever be, heh heh heh")
            
        libtcod.console_set_default_foreground(0, libtcod.white)
        libtcod.console_print_ex(0, 2, 2, libtcod.BKGND_NONE, libtcod.LEFT, "Merchant!")

        libtcod.console_set_default_foreground(0, screen_darkgray)
        libtcod.console_print_ex(0, 42, 3, libtcod.BKGND_NONE, libtcod.LEFT, "Gold: " + str(player.current_gold) + "g")  
            
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while True:
   
        numequip = (len(_globals.vendorEnt.equipment.list) - _globals.vendorEnt.equipment.list.count(None))
        numitems = len(_globals.vendorEnt.inventory.items)
        numpages = int((numitems + numequip)/ itemsperpage) + 1
        
        if numitems == 0 and numequip == 0:
            return results
        
        #re-draw (clear) inventory space
        for y in range(13, 13+itemsperpage):
            for x in range(3, 30):
                if y % 2 == 0: #even
                    libtcod.console_set_default_background(0, screen_midgray)
                else: #odd
                    libtcod.console_set_default_background(0, screen_lightgray)
                libtcod.console_print_ex(0, x, y, libtcod.BKGND_SET, libtcod.LEFT, " ")
                
        #first inventory row
        y = 13  
        
        #draw items and equipment list
        libtcod.console_set_default_foreground(0, libtcod.black)

        #process equipment in inventory list
        if numequip > 0:
            #print in inventory list
            if currentpage == 1:
                for x in range (0 + (itemsperpage * (currentpage-1)), numequip):
                    itm = get_item_at("equipment", x, _globals.vendorEnt)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, get_name_string(itm, _globals.names_list))    
                    y += 1

        #process inventory
        libtcod.console_set_default_foreground(0, libtcod.black)
        if numitems > 0:
            start  = 0 + (itemsperpage * (currentpage-1))
            end = start + itemsperpage
            if currentpage == 1: end -= numequip   
            for x in range (start, end):
                if x < len(_globals.vendorEnt.inventory.items):
                    itm = get_item_at("inventory", x, _globals.vendorEnt)
                    libtcod.console_print_ex(0, 3, y, libtcod.BKGND_NONE, libtcod.LEFT, get_name_string(itm, _globals.names_list))    
                    y += 1   
                
        mx = mouse.cx
        my = mouse.cy

        # elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
        #     cap = numitems -1
        #     if currentpage == 1: cap += numequip
        #     if index < cap: index += 1
        #     if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        # elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
        #     if index > 0: index -= 1
        #     if line == 13 and currentpage > 1: currentpage -= 1


        #if the mouse is in the right position, use mouseindex
        if my >= 13 and my < (13 + itemsperpage):
            if mx >= 3 and mx < 30:
                mouse_index = my-13
                cap = numitems 
                if currentpage == 1: cap += numequip
                if mouse_index <= cap: index = mouse_index

        #iindex = index
        #green selection line
        strname = ""
        iindex = index
        if numequip > 0:
            if currentpage == 1:
                if index < numequip: 
                    system = "equipment"
                    strname = "> "
                else:   
                    system = "inventory"
                    iindex = index - numequip
        else:
            system = "inventory"
            iindex = index - numequip
        
        #get the item at the current index
        item = get_item_at(system, iindex, _globals.vendorEnt)
        line = 13 + (index%itemsperpage)
        
        #draw the green selection line
        strname += get_name_string(item, _globals.names_list)
        libtcod.console_set_default_background(0, screen_green)
        libtcod.console_set_default_foreground(0, libtcod.black)
        libtcod.console_print_ex(0, 3, line, libtcod.BKGND_SET, libtcod.LEFT, "                           ")  
        if item.item.take_at_buy == False: libtcod.console_print_ex(0, 3, line, libtcod.BKGND_NONE, libtcod.LEFT, strname + " " + chr(236))
        else: libtcod.console_print_ex(0, 3, line, libtcod.BKGND_NONE, libtcod.LEFT, strname + " x" + str(item.item.vendor_count))
        
        #clear the description area
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, "                          ")
        
        for y in range (15, 32):
            libtcod.console_print_ex(0, 44, y, libtcod.BKGND_SET, libtcod.CENTER, "                          ")

        
        libtcod.console_set_default_background(0, screen_midgray)
        libtcod.console_set_default_foreground(0, libtcod.white)
        
        libtcod.console_print_ex(0, 44, 13, libtcod.BKGND_SET, libtcod.CENTER, " " + chr(item.char) + " " + _globals.names_list[item.name] + " ")
        
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)

        #get and draw the description
        lines = item.item.description_lines
        
        y = 15
        for l in lines:
            libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
            y+=1           
            
        if _globals.names_list[item.name] == item.name: #only write the effect if its identified    
            if item.item.effect_lines:
                y += 1 #start the effect text after the description text ends.
                for l in item.item.effect_lines:
                    libtcod.console_print_ex(0, 31, y, libtcod.BKGND_SET, libtcod.LEFT, l) 
                    y+=1  
                #y += 1
            
        if item.equippable:
            libtcod.console_set_default_background(0, screen_darkgray)
            libtcod.console_set_default_foreground(0, screen_lightgray)
    
            #if no eq to comapre to, the difference is just the bonus of the item in question
            diff_atk = item.equippable.power_bonus
            diff_def = item.equippable.defense_bonus
            diff_mhp = item.equippable.max_hp_bonus
            diff_spd = item.equippable.speed_bonus
            diff_lck = item.equippable.luck_bonus
            diff_cap = item.equippable.capacity_bonus
            
            comp = None
            for eq in player.equipment.list:
                if eq.equippable.slot == item.equippable.slot:
                   comp = eq
                   break

            comp_total = 0
            item_total = 0

            #if there is eq to compare to, and it's not the same item, list its stats, and the difference is comp - current
            if comp and comp != item:
                x = 45                
            
                diff_atk = item.equippable.power_bonus - comp.equippable.power_bonus
                diff_def = item.equippable.defense_bonus - comp.equippable.defense_bonus
                diff_mhp = item.equippable.max_hp_bonus - comp.equippable.max_hp_bonus
                diff_spd = item.equippable.speed_bonus - comp.equippable.speed_bonus 
                diff_lck = item.equippable.luck_bonus - comp.equippable.luck_bonus
                diff_cap = item.equippable.capacity_bonus - comp.equippable.capacity_bonus
                item_total = (item.equippable.power_bonus + item.equippable.defense_bonus + 
                    item.equippable.max_hp_bonus + item.equippable.speed_bonus + item.equippable.luck_bonus + item.equippable.capacity_bonus) 
                comp_total = (comp.equippable.power_bonus + comp.equippable.defense_bonus + 
                    comp.equippable.max_hp_bonus + comp.equippable.speed_bonus + comp.equippable.luck_bonus + comp.equippable.capacity_bonus) 

                if item_total > comp_total:
                    libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    libtcod.console_print_ex(0, 37, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
                    libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, comp.item.comp_name)
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                
                elif item_total < comp_total:
                    libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, comp.item.comp_name)
                    libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, 37, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                
                #print the comp stats
                if True:
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    libtcod.console_print_ex(0, x, y+3, libtcod.BKGND_SET, libtcod.LEFT, "ATK  ")
                    libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "DEF  ")
                    libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "MHP  ")
                    libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "SPD  ")
                    libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "LCK  ")
                    libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "CAP  ")
                    
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+3, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.power_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.defense_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.max_hp_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.speed_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.luck_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+7, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(comp.equippable.capacity_bonus))
                    
            x = 41
            if comp and comp != item: x = 37
            
            if item_total > comp_total:
                libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
            elif item_total < comp_total:
                libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)
            else:
                libtcod.console_set_default_foreground(0, screen_lightgray)
                libtcod.console_print_ex(0, x, y+1, libtcod.BKGND_SET, libtcod.LEFT, item.item.comp_name)

            libtcod.console_set_default_foreground(0, screen_lightgray)
            libtcod.console_print_ex(0, x, y+3, libtcod.BKGND_SET, libtcod.LEFT, "ATK ")
            libtcod.console_print_ex(0, x, y+4, libtcod.BKGND_SET, libtcod.LEFT, "DEF ")
            libtcod.console_print_ex(0, x, y+5, libtcod.BKGND_SET, libtcod.LEFT, "MHP ")
            libtcod.console_print_ex(0, x, y+6, libtcod.BKGND_SET, libtcod.LEFT, "SPD ")
            libtcod.console_print_ex(0, x, y+7, libtcod.BKGND_SET, libtcod.LEFT, "LCK ")
            libtcod.console_print_ex(0, x, y+8, libtcod.BKGND_SET, libtcod.LEFT, "CAP ")

            #print the item stats    
            if True:

                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_atk > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_atk < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+3, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.power_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_def > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_def < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+4, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.defense_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_mhp > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_mhp < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+5, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.max_hp_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_spd > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_spd < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+6, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.speed_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_lck > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_lck < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+7, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.luck_bonus))
                    
                    libtcod.console_set_default_foreground(0, screen_lightgray)
                    if diff_cap > 0: libtcod.console_set_default_foreground(0, libtcod.lighter_green)
                    if diff_cap < 0: libtcod.console_set_default_foreground(0, libtcod.lighter_red)
                    libtcod.console_print_ex(0, x+5, y+8, libtcod.BKGND_SET, libtcod.RIGHT, str(item.equippable.capacity_bonus))
                
        #re-draw (clear) possible action items
        libtcod.console_set_default_background(0, screen_darkgray)
        libtcod.console_set_default_foreground(0, screen_lightgray)
        libtcod.console_print_ex(0, 31, 32, libtcod.BKGND_SET, libtcod.LEFT, "Cost : " + str(item.item.cost) + "g    ")
        libtcod.console_print_ex(0, 31, 34, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to purchase")
        libtcod.console_print_ex(0, 31, 36, libtcod.BKGND_SET, libtcod.LEFT, "[Escape] to close")
        
        libtcod.console_set_default_foreground(0, libtcod.light_flame)
        libtcod.console_print_ex(0, 31, 31, libtcod.BKGND_SET, libtcod.LEFT, "Current Gold: " + str(player.current_gold) + "g")
        #libtcod.console_flush()
        
        #draw relevant action items
        libtcod.console_set_default_foreground(0, libtcod.light_green)
        if (item.item and item.item.use_function) or item.equippable: libtcod.console_print_ex(0, 31, 34, libtcod.BKGND_SET, libtcod.LEFT, "[Enter] to purchase")
        
        #Render changes
        libtcod.console_flush()   
        
        #Check for input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)    

        left_click = mouse.lbutton_pressed

        if key.vk == libtcod.KEY_ESCAPE or chr(key.c) == "v":
            #results.append({'ignore': 0})
            return results
            
        elif key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER or left_click: 
            buy_item(player, item)
            
            # if left_click:
            #     if not (my >= 13 and my < (13 + itemsperpage)): break
            #     if not(mx >= 3 and mx < 30): break
                
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            cap = numitems -1
            if currentpage == 1: cap += numequip
            if index < cap: index += 1
            if line == 36 and currentpage + 1 <= numpages: currentpage = currentpage + 1

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            if index > 0: index -= 1
            if line == 13 and currentpage > 1: currentpage -= 1

def buy_item(player, item):
    results = []

    #libtcod.console_print_ex(0, 6, 5, libtcod.BKGND_NONE, libtcod.LEFT, "Welcome, weary contestant, to my humble shop.")

    if player.current_gold >= item.item.cost and item.item.vendor_count > 0: #if you have the gold, and the vendor has the item, take the gold and give the item
        if item.name == _globals.last_item_purchased:
            _globals.amt_purchased += 1
        else:
            _globals.amt_purchased = 1
        stacked = False
        for i in player.inventory.items:
            if i.name == item.name and i.item.stackable: #stackable items
                i.count += item.item.count
                stacked = True   
                #dialogue from the vendor
                libtcod.console_set_default_foreground(0, libtcod.light_green)
                libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_SET, libtcod.LEFT, "Ah, a good choice. Anything else I can do for ya?")
                libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "Purchased " + item.name + " x " + str(_globals.amt_purchased) + "                              ")
                libtcod.console_flush()
                results.append({
                    'item_added': item,
                    'message': Message('You purchased the {0}!'.format(item.name), libtcod.blue)
                })
                _globals.last_item_purchased = item.name
                player.inventory.items.append(item)
                player.current_gold -= item.item.cost
                
                if item.item.take_at_buy == False:
                    return
                else:
                    item.item.vendor_count -= 1
                    
        if not stacked:
            if len(player.inventory.items) >= player.inventory.max_capacity: #if you don't have the room, take neither gold nor item
                
                #dialogue from the vendor
                libtcod.console_set_default_foreground(0, libtcod.light_flame)
                libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_SET, libtcod.LEFT, "Seems you don't have the pockets for that one.    ")
                libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "                                                ")
                libtcod.console_flush()        
                
                results.append({
                    'item_added': None,
                    'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
                    
                })

            else: #non stackable items
                #dialogue from the vendor
                libtcod.console_set_default_foreground(0, libtcod.light_green)
                libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_SET, libtcod.LEFT, "Ah, a good choice. Anything else I can do for ya?")
                libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "Purchased " + item.name + " x " + str(_globals.amt_purchased) + "                              ")
                libtcod.console_flush()
                results.append({
                    'item_added': item,
                    'message': Message('You purchased the {0}!'.format(item.name), libtcod.blue)
                })
                _globals.last_item_purchased = item.name
                player.inventory.items.append(item)
                player.current_gold -= item.item.cost
                
                if item.item.take_at_buy == False:
                    return
                else:
                    item.item.vendor_count -= 1

    elif item.item.count == 0: #if the vendor runs out, you don't get the item
        libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_SET, libtcod.LEFT, "Seems you've bought me out of that one.             ")
        libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "                                                    ")

        # results.addpend({
        #     'item_added': None,
        #     'message': Message('The vendor does not have any more of that item available', libtcod.yellow)

        # })

    else: #if you don't have the gold, you don't get the item
    
        #dialogue from the vendor
        libtcod.console_set_default_foreground(0, libtcod.light_flame)
        libtcod.console_print_ex(0, 6, 7, libtcod.BKGND_SET, libtcod.LEFT, "Seems you don't have enough gold for that one.      ")
        libtcod.console_print_ex(0, 6, 9, libtcod.BKGND_NONE, libtcod.LEFT, "                                                    ")
        libtcod.console_flush()

    libtcod.console_flush()
    return results

class Shady_Vendor:
    game_map.boss_room_passed = False