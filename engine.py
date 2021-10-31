import pygame
import tcod as libtcod
import textwrap
import time

#imports
import _globals
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, message_log_history
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables, get_unidentified_names, get_render_colors, load_customfont
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box, inventory_menu, character_screen, game_options, origin_options, intro, character_name, help_menu
from render_functions import get_all_at, RenderOrder, clear_all, render_all
from map_objects.tile import Door
from equipment_slots import EquipmentSlots
from ammo_functions import Fire_And_Preference

from random import randint
import copy

def player_turn_end(player, player_turn_results, game_map, message_log):
    
    player.turn_count += 1            
                    
    for entity in _globals.entities:
        if entity.fighter:
            if entity.fighter.hp > 0:
                for con in entity.conditions:
                    if con.active:
                        player_turn_results.extend(con.enact())
                        
    #process turn results for conditions
    if player_turn_results:
        for player_turn_result in player_turn_results:
            damage = player_turn_result.get('damage')
            if damage:
                dead_entity = damage[0].get('dead')
                print (dead_entity.name + 'died')
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity, game_map)
                else:
                    if dead_entity.fighter:


                            score_gained = int(dead_entity.fighter.xp * _globals.constants['options_xp_multiplier'] * _globals.constants['xp_to_score_ratio'])   

                            #assign the camera operator to the cam variable
                            cam = None
                            for entity in _globals.entities:
                                if entity.name == "Camera Op.":
                                    cam = entity
                                    break
                            
                            #if a camera operator was located ...
                            if cam:

                                #assume the camera op did not see the kill
                                seen = False
                                
                                #check if camera op saw the kill
                              
                                #initialize a fov around the camera operator using the same constants the player uses
                                cam_fov = initialize_fov(game_map)
                                recompute_fov(cam_fov, cam.x, cam.y, _globals.constants['fov_radius'], _globals.constants['fov_light_walls'],
                                        _globals.constants['fov_algorithm'])
                                        
                                #assign the killx/killy positions using dead_entity
                                (kill_x, kill_y) = (dead_entity.x, dead_entity.y)
                                
                                #check if killx/killy is in the camera_fov
                                seen = libtcod.map_is_in_fov(cam_fov, kill_x, kill_y)
                                
                                # if the camera op did see the kill, multiply score gained by the 'seen kill' mulitiplier
                                if seen: score_gained = int(score_gained * _globals.constants['kill_seen_by_camera_mult'])
                            
                            #ensure each kill gives at least one point
                            if score_gained < 1: score_gained = 1
                            
                            #add the end result to the player score
                            player.score += score_gained
                        
                message = kill_monster(dead_entity, player)
                    
                message_log.add_message(message)

def render_refresh(con, panel, mouse, player, game_map, fov_map, fov_recompute, message_log, game_state):
    if fov_recompute:
        recompute_fov(fov_map, player.x, player.y, _globals.constants['fov_radius'], _globals.constants['fov_light_walls'],
                        _globals.constants['fov_algorithm'])
                
    render_all(con, panel, player, game_map, fov_map, fov_recompute, message_log, mouse, game_state)


    libtcod.console_flush()

    clear_all(con)        

def play_game(player, game_map, message_log, game_state, con, panel):
    
    
    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None
    ranged_weapon = None    #used to keep track of which (if any) ranged weapon is being fired 
    
    player_turn_results = []
    
    #pygame.mixer.init()
    #pygame.mixer.music.load('audio/sfx/bgchatter.mp3')
    #pygame.mixer.music.play(-1)
    pygame.init()

    while not libtcod.console_is_window_closed():

        _globals.constants['tick'] = int(pygame.time.get_ticks()/100)

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, _globals.constants['fov_radius'], _globals.constants['fov_light_walls'],
                          _globals.constants['fov_algorithm'])
                 
        render_all(con, panel, player, game_map, fov_map, fov_recompute, message_log, mouse, game_state)

        fov_recompute = False
 
        libtcod.console_flush()

        clear_all(con)

        action = handle_keys(key, game_state)
        #if len(action) > 0: print(action)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        #drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fire = action.get('fire')
        fullscreen = action.get('fullscreen')
        key_targeting = action.get('key_targeting')
        close = action.get('close')
        kick = action.get('kick')
        messagelog = action.get('messagelog')
        help = action.get('show_help')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []


        # TODO :: work on auto-walker ..
        # code below almost works.. but a-star will never END on the targeted tile, so checking for mx/my == px/py will not work
        #not sure how to solve for this at the moment.

        if left_click:
            (mx, my) = (mouse.cx, mouse.cy)

            if (mx, my) == (player.x, player.y):
                player_turn_results.extend(inventory_menu(player, message_log, fov_map))

        #     print(str((mx,my)))
        #     if libtcod.map_is_in_fov(fov_map, mx, my):
        #         spot = Entity(mx, my, 0, libtcod.black, 'spot')
        #         while (True):
        #             if player.x != mx and player.y != my:
        #                 player.move_astar(spot, entities, game_map)
        #                 player_turn_end(player, player_turn_results, game_map, constants, entities, message_log)
        #                 fov_recompute = True
        #                 render_refresh(con, panel, mouse, entities, player, game_map, fov_map, fov_recompute, message_log, constants, game_state, names_list, colors_list)
        #                 time.sleep(0.0255)
        #             else:
        #                 break
                
                        

        if move:
            if game_state == GameStates.PLAYERS_TURN: 
                
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy

                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(destination_x, destination_y)

                    if target:  
                        if target.name == "Camera Op.":
                            (tx, ty) = (player.x, player.y)
                            player.x = target.x
                            player.y = target.y
                            target.x = tx
                            target.y = ty
                        else:
                            attack_results = player.fighter.attack(target)
                            player_turn_results.extend(attack_results)     
                    else:
                        player.move(dx, dy)

                        fov_recompute = True
                        
                    #player_turn_end(player, player_turn_results, game_map, constants)
                    game_state = GameStates.ENEMY_TURN
                else:
                    if game_map.tiles[destination_x][destination_y].door:
                        if not game_map.tiles[destination_x][destination_y].door.is_open:
                            game_map.tiles[destination_x][destination_y].door.toggle_open(game_map, destination_x, destination_y)
                            fov_recompute = True
                            fov_map = initialize_fov(game_map)
                    
                player_turn_end(player, player_turn_results, game_map, message_log)
            
            elif game_state == GameStates.KEYTARGETING:
                dx, dy = move
                destination_x = targeter.x + dx
                destination_y = targeter.y + dy
                
                if (destination_x >= 0 and destination_x <= _globals.constants['map_width']) and (destination_y >= 0 and destination_y <= _globals.constants['map_height']):
                    targeter.move(dx, dy)
                    fov_recompute = True
                    libtcod.console_set_default_foreground(panel, libtcod.light_gray)

        elif wait:
            player_turn_end(player, player_turn_results, game_map, message_log)
            game_state = GameStates.ENEMY_TURN
            
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in _globals.entities:
          
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        elif key_targeting:
            previous_game_state = game_state
            game_state = GameStates.KEYTARGETING
            #create 'targeting' entity
            targeter = Entity(player.x, player.y, 233, (204,153,51), 'Targeter', blocks=False, render_order=RenderOrder.TARGETING)
            _globals.entities.append(targeter)
        
        elif messagelog:
            message_log_history(message_log)
            
        elif kick:
            if game_state == GameStates.KICKING:
                
                dx, dy = kick
              
                kickx, kicky  = player.x + dx, player.y + dy             
                
                target = None
                for entity in _globals.entities:
                    if entity.x == kickx and entity.y == kicky and entity.stairs == False:
                        target = entity
                        break
                    
                if target == None:
                    if game_map.tiles[kickx][kicky].door:
                        if game_map.tiles[kickx][kicky].door.is_open:
                            message_log.add_message(Message('There is nothing there to kick.', libtcod.red))
                        else:
                            message_log.add_message(Message('You kick the door. Ouch!', libtcod.red))
                            player_turn_results.extend(player.fighter.take_damage(2))
                    elif game_map.tiles[kickx][kicky].blocked:
                        message_log.add_message(Message('Kicking a wall does not feel good.', libtcod.red))
                        player_turn_results.extend(player.fighter.take_damage(2))
                    else:
                        message_log.add_message(Message('Nothing there to kick.', libtcod.yellow))
                else:
                    if target.fighter:
                        message_log.add_message(Message('The  ' + target.name + ' dodges your kick.', libtcod.gray))
                    else:
                        if not game_map.tiles[target.x+dx][target.y+dy].block_sight:
                            target.move(dx, dy)
                            if game_map.tiles[kickx][kicky].door: fov_recompute = True
                
                if previous_game_state == GameStates.PLAYERS_TURN:
                    player_turn_end(player, player_turn_results, game_map, message_log)
                    game_state = GameStates.ENEMY_TURN
                else:
                    game_state = previous_game_state
                
            else:   
                previous_game_state = game_state
                game_state = GameStates.KICKING
                
        elif help:
            help_menu()

        elif close:
            if game_state == GameStates.CLOSING:
                
                dx, dy = close
              
                closex, closey  = player.x + dx, player.y + dy             
                
                if game_map.tiles[closex][closey].door:
                    if game_map.tiles[closex][closey].door.is_open:
                        blocked = False
                        for entity in _globals.entities:
                            if entity.x == closex and entity.y == closey:
                                blocked = True
                                break
                        if not blocked:        
                            game_map.tiles[closex][closey].door.toggle_open(game_map, closex, closey)
                            message_log.add_message(Message('You close the door.', libtcod.white))
                            fov_map = initialize_fov(game_map)
                            fov_recompute = True
                        else:
                            message_log.add_message(Message('There is something in the way.', libtcod.lighter_red))
                    else:
                        message_log.add_message(Message('The door is already closed.', libtcod.white))
                else:
                    #check for chests etc .. other objects that could be closed
                    message_log.add_message(Message('There is nothing there to close.', libtcod.lighter_red))
                    
                if previous_game_state == GameStates.PLAYERS_TURN:
                    player_turn_end(player, player_turn_results, game_map, message_log)
                    game_state = GameStates.ENEMY_TURN
                else:
                    game_state = previous_game_state
                
            else:   
                previous_game_state = game_state
                game_state = GameStates.CLOSING
        
        elif fire:
            if game_state == GameStates.FIRING:
                
                #ranged_weapon should be assigned when game_state goes from player_turn to firing..
                #check "for eq in player.equipment.list:" loop near line 310 engine.py on error
                if not ranged_weapon:
                    print("dafuq? ... line 309 engine .. no ranged weapon?!")

                #get direction from the player_turn_results 'fire' key    
                dx, dy = fire
                
                current_pref = globals.constants['options_ammo_preference']

                FnP = Fire_And_Preference()
                if str(FnP) == "None":
                    message_log.add_message(Message('You do not have anything to shoot.', libtcod.light_red))

                elif str(FnP) == "exit":
                    print("Canceled")

                else:
                    if FnP != current_pref: message_log.add_message(Message('You have updated your default ammo preference.', libtcod.light_gray))

                    ammo = None

                    for i in player.inventory.items:
                        if i.name == FnP:
                            ammo = i
                            if i.item.count == 1:
                                _globals.constants['options_ammo_preference'] = None
                                
                                for q in player.inventory.items:
                                    if q.name == 'Quiver':
                                        q.item.effect_lines = textwrap.wrap("  Firing preference is currently unassigned.", 26) 
                                        break

                            player.inventory.remove_item(i)
                            break

                    hit = False
                    lost = False

                    #loop through the range of the weapon in question
                    for r in range(1, ranged_weapon.item.range+2):
                        if hit or lost: break
                        
                        sx = player.x + (dx * r)
                        sy = player.y + (dy * r)
                        
                        if game_map.tiles[sx][sy].block_sight or game_map.tiles[sx][sy].blocked or r == ranged_weapon.item.range+1:
                            lost = True

                            if ammo.item.ammo.retrievable: 
                                ia = copy.deepcopy(ammo)
                                ia.item.count = 1
                                (ix, iy) = (sx-dx, sy-dy)
                                (ia.x, ia.y) = (ix, iy)
                                _globals.entities.append(ia)
                                break
                        else:
                            for ent in _globals.entities:
                                if ent.fighter:
                                    if ent.x == sx and ent.y == sy:
                                        hit = True
                                        
                                        player_turn_results.extend(ammo.item.ammo.hit_function.hit(shooter=player, target=ent, constants=globals.constants))
                                    
                if previous_game_state == GameStates.PLAYERS_TURN:
                    player_turn_end(player, player_turn_results, game_map, message_log)
                    game_state = GameStates.ENEMY_TURN
                else:
                    game_state = previous_game_state
                
            else:   
            
                for eq in player.equipment.list:
                    
                    if eq.equippable.slot == EquipmentSlots.MAIN_HAND or eq.equippable.slot == EquipmentSlots.OFF_HAND:
                        if eq.item.range > 0:
                            ranged_weapon = eq
                            break
                    
                if ranged_weapon:
                    previous_game_state = game_state
                    game_state = GameStates.FIRING
                else:
                    #hip firing goes here
                    message_log.add_message(Message('You do not have a ranged weapon equipped.', libtcod.lighter_red))
                    
        
        elif show_inventory:
            player_turn_results.extend(inventory_menu(player,fov_map, message_log))

        #if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
        #        player.inventory.items):
        #    item = player.inventory.items[inventory_index]
        #
        #    if game_state == GameStates.SHOW_INVENTORY:
        #        player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list, message_log=message_log))
        #    elif game_state == GameStates.DROP_INVENTORY:
        #        player_turn_results.extend(player.inventory.drop_item(item))

        elif take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in _globals.entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    _globals.entities = game_map.next_floor(player, message_log)

                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        elif level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        elif show_character_screen:
            player_turn_results.extend(character_screen(player, game_map.dungeon_level))

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state in (GameStates.TARGETING, GameStates.KEYTARGETING):
                if game_state == GameStates.KEYTARGETING: 
                    _globals.entities.remove(targeter)
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, game_map, message_log, game_state)

                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    if dead_entity.fighter:
                        
                        #if dead_entity.name == "Camera Op.":
                        #    boo = pygame.mixer.Sound('audio/sfx/boo1.mp3')
                        #    pygame.mixer.Sound.play(boo)
                            
                        score_gained = int(dead_entity.fighter.xp * _globals.constants['options_xp_multiplier'] * _globals.constants['xp_to_score_ratio'])   

                        #assign the camera operator to the cam variable
                        cam = None
                        for entity in _globals.entities:
                            if entity.name == "Camera Op.":
                                cam = entity
                                break
                        
                        #if a camera operator was located ...
                        if cam:

                            #assume the camera op did not see the kill
                            seen = False
                            
                            #check if camera op saw the kill
                          
                            #initialize a fov around the camera operator using the same constants the player uses
                            cam_fov = initialize_fov(game_map)
                            recompute_fov(cam_fov, cam.x, cam.y, _globals.constants['fov_radius'], _globals.constants['fov_light_walls'],
                                    _globals.constants['fov_algorithm'])
                                    
                            #assign the killx/killy positions using dead_entity
                            (kill_x, kill_y) = (dead_entity.x, dead_entity.y)
                            
                            #check if killx/killy is in the camera_fov
                            seen = libtcod.map_is_in_fov(cam_fov, kill_x, kill_y)
                            
                            # if the camera op did see the kill, multiply score gained by the 'seen kill' mulitiplier
                            if seen: score_gained = int(score_gained * _globals.constants['kill_seen_by_camera_mult'])
                        
                        #ensure each kill gives at least one point
                        if score_gained < 1: score_gained = 1
                        
                        #add the end result to the player score
                        player.score += score_gained
                    
                    message = kill_monster(dead_entity, player)
                    
                message_log.add_message(message)

            if item_added:
                _globals.entities.remove(item_added)
                
                player_turn_end(player, player_turn_results, game_map, message_log)
                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                
                player_turn_end(player, player_turn_results, game_map, message_log)
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                
                _globals.entities.append(item_dropped)
                
                player_turn_end(player, player_turn_results, game_map, message_log)
                game_state = GameStates.ENEMY_TURN

            if equip:
                print("equip outside of inventory?!")

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled.'))
                fov_recompute = True

            if xp:
                axp = int(xp * _globals.constants['options_xp_multiplier'])
                leveled_up = player.level.add_xp(axp)
                message_log.add_message(Message('You gain {0} experience points.'.format(axp)))
                
                if leveled_up:
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:   
            
            enemy_turn_results = []
            for entity in _globals.entities:
                #proccess AI and turns
                if entity.name == "Camera Op." or libtcod.map_is_in_fov(fov_map, entity.x, entity.y):              
                    if entity.ai:                 
                        if entity.fighter:
                            if player.fighter: #if player isn't dead ..

                                entity.fighter.timer = entity.fighter.timer + entity.fighter.speed

                                while entity.fighter.timer >= player.fighter.speed:

                                    enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map)

                                    entity.fighter.timer = entity.fighter.timer - player.fighter.speed

                                    render_refresh(con, panel, mouse, player, game_map, fov_map, fov_recompute, message_log, game_state)
                                    time.sleep(0.0255)

                                    if enemy_turn_results != None:
                                        for enemy_turn_result in enemy_turn_results:
                                            message = enemy_turn_result.get('message')
                                            dead_entity = enemy_turn_result.get('dead')

                                            if message:
                                                message_log.add_message(message)

                                            if dead_entity:
                                                if dead_entity == player or dead_entity.name == "Player":
                                                    message, game_state = kill_player(dead_entity, game_map, _globals.constants)
                                                else:
                                                    message = kill_monster(dead_entity, player)

                                                message_log.add_message(message)

                                                if game_state == GameStates.PLAYER_DEAD:
                                                    break

            if game_state == GameStates.PLAYER_DEAD:
                break
            else:                
                game_state = GameStates.PLAYERS_TURN


def main():

    _globals.init()          # Call only once
    _globals.load_customfont()

    libtcod.console_set_custom_font('fontplus.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW, 16, 30)
    
    libtcod.console_init_root(_globals.constants['screen_width'], _globals.constants['screen_height'], _globals.constants['window_title'], False)

    con = libtcod.console.Console(_globals.constants['screen_width'], _globals.constants['screen_height'])
    panel = libtcod.console.Console(_globals.constants['screen_width'], _globals.constants['panel_height'])
    
    player = None
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, _globals.constants['screen_width'],
                      _globals.constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, _globals.constants['screen_width'], _globals.constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                if intro():
                    if not game_options() == "nah":
                        if not origin_options() == "nah":
                            if not character_name() == 'nah':
                                player, _globals.entities, game_map, message_log, game_state = get_game_variables()
                                game_state = GameStates.PLAYERS_TURN

                                show_main_menu = False
            elif load_saved_game:
                try:
                    player, _globals.entities, game_map, message_log, game_state, _globals.constants = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True

            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, game_map, message_log, game_state, con, panel)

            show_main_menu = True

#
if __name__ == '__main__':
    main()