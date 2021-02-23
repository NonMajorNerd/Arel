import tcod as libtcod

#imports
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, message_log_history
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables, get_unidentified_names, get_render_colors
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box, inventory_menu, game_options
from render_functions import get_all_at, RenderOrder, clear_all, render_all
from map_objects.tile import Door

from random import randint

def player_turn_end(player, player_turn_results):
    
    player.turn_count += 1            

    if len(player.conditions) > 0:
        for condition in player.conditions:
            if condition.active:
                player_turn_results.extend(condition.enact())   


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants, names_list, colors_list):

    fov_recompute = True
    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None
    player_turn_results = []
    
    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])
                 
        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, constants['colors'], constants['options_tutorial_enabled'], game_state, names_list, colors_list)

        fov_recompute = False
 
        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        wait = action.get('wait')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        key_targeting = action.get('key_targeting')
        close = action.get('close')
        kick = action.get('kick')
        messagelog = action.get('messagelog')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        player_turn_results = []

        if move:
            if game_state == GameStates.PLAYERS_TURN: 
                
                dx, dy = move
                destination_x = player.x + dx
                destination_y = player.y + dy

                if not game_map.is_blocked(destination_x, destination_y):
                    target = get_blocking_entities_at_location(entities, destination_x, destination_y)

                    if target:  
                        if target.name == "Camera Op.":
                            (tx, ty) = (player.x, player.y)
                            player.x = target.x
                            player.y = target.y
                            target.x = tx
                            target.y = ty
                        else:
                            attack_results = player.fighter.attack(target, constants)
                            player_turn_results.extend(attack_results)     
                    else:
                        player.move(dx, dy)

                        fov_recompute = True
                        dijkstra_recompute = True

                    game_state = GameStates.ENEMY_TURN
                else:
                    if game_map.tiles[destination_x][destination_y].door:
                        if not game_map.tiles[destination_x][destination_y].door.is_open:
                            game_map.tiles[destination_x][destination_y].door.toggle_open(game_map, destination_x, destination_y)
                            fov_recompute = True
                            dijkstra_recompute = True
                            fov_map = initialize_fov(game_map)
                    
                player_turn_end(player, player_turn_results)
            
            elif game_state == GameStates.KEYTARGETING:
                dx, dy = move
                destination_x = targeter.x + dx
                destination_y = targeter.y + dy
                
                if (destination_x >= 0 and destination_x <= constants['map_width']) and (destination_y >= 0 and destination_y <= constants['map_height']):
                    targeter.move(dx, dy)
                    fov_recompute = True
                    libtcod.console_set_default_foreground(panel, libtcod.light_gray)

        elif wait:
            player_turn_end(player, player_turn_results)
            game_state = GameStates.ENEMY_TURN
            
        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity, names_list)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if key_targeting:
            previous_game_state = game_state
            game_state = GameStates.KEYTARGETING
            #create 'targeting' entity
            targeter = Entity(player.x, player.y, 233, (204,153,51), 'Targeter', blocks=False, render_order=RenderOrder.TARGETING)
            entities.append(targeter)
        
        if messagelog:
            message_log_history(message_log)
            
        if kick:
            if game_state == GameStates.KICKING:
                
                dx, dy = kick
              
                kickx, kicky  = player.x + dx, player.y + dy             
                
                target = None
                for entity in entities:
                    if entity.x == kickx and entity.y == kicky:
                        target = entity
                        break
                    
                if target == None:
                    if game_map.tiles[kickx][kicky].door:
                        if game_map.tiles[kickx][kicky].door.is_open:
                            message_log.add_message(Message('There is nothing there to kick.', libtcod.red))
                        else:
                            message_log.add_message(Message('You kick the door. Ouch!', libtcod.red))
                    elif game_map.tiles[kickx][kicky].blocked:
                        message_log.add_message(Message('Kicking a wall does not feel good.', libtcod.red))
                        player_turn_results.extend(player.fighter.take_damage(3))
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
                    player_turn_end(player, player_turn_results)
                    game_state = GameStates.ENEMY_TURN
                else:
                    game_state = previous_game_state
                
            else:   
                previous_game_state = game_state
                game_state = GameStates.KICKING

        if close:
            if game_state == GameStates.CLOSING:
                
                dx, dy = close
              
                closex, closey  = player.x + dx, player.y + dy             
                
                if game_map.tiles[closex][closey].door:
                    if game_map.tiles[closex][closey].door.is_open:
                        game_map.tiles[closex][closey].door.toggle_open(game_map, closex, closey)
                        message_log.add_message(Message('You close the door.', libtcod.white))
                        fov_map = initialize_fov(game_map)
                        fov_recompute = True
                    else:
                        message_log.add_message(Message('The door is already closed.', libtcod.white))
                else:
                    #check for chests etc .. other objects that could be closed
                    message_log.add_message(Message('There is nothing there to close.', libtcod.lighter_red))
                    
                if previous_game_state == GameStates.PLAYERS_TURN:
                    player_turn_end(player, player_turn_results)
                    game_state = GameStates.ENEMY_TURN
                else:
                    game_state = previous_game_state
                
            else:   
                previous_game_state = game_state
                game_state = GameStates.CLOSING

        if show_inventory:
            player_turn_results.extend(inventory_menu(player, entities, fov_map, names_list, colors_list))

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(
                player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item, entities=entities, fov_map=fov_map, names_list=names_list))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(player, message_log, constants, names_list, colors_list)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('There are no stairs here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y, names_list=names_list)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state in (GameStates.TARGETING, GameStates.KEYTARGETING):
                if game_state == GameStates.KEYTARGETING: 
                    entities.remove(targeter)
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state, constants)

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
                    message, game_state = kill_player(dead_entity, game_map, constants)
                else:
                    message = kill_monster(dead_entity, player)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if dequipped:
        
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))
                fov_recompute = True

            if xp:
                axp = int(xp * constants['options_xp_multiplier'])
                leveled_up = player.level.add_xp(axp)
                message_log.add_message(Message('You gain {0} experience points.'.format(axp)))

                if leveled_up:
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

        if game_state == GameStates.ENEMY_TURN:   
            
            for entity in entities:
                if entity.name == "Camera Op." or libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
                    if entity.ai:                 
                        if entity.fighter:
                            entity.fighter.timer += entity.fighter.speed
                            while entity.fighter.timer >= player.fighter.speed:
                                enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities, constants)
                                entity.fighter.timer -= player.fighter.speed
                                
                                if enemy_turn_results != None:
                                    for enemy_turn_result in enemy_turn_results:
                                        message = enemy_turn_result.get('message')
                                        dead_entity = enemy_turn_result.get('dead')

                                        if message:
                                            message_log.add_message(message)

                                        if dead_entity:
                                            if dead_entity == player:
                                                message, game_state = kill_player(dead_entity, game_map, constants)
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
    constants = get_constants()
    names_list = get_unidentified_names()
    colors_list = get_render_colors()

    libtcod.console_set_custom_font('fontplus.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW, 16, 30)
    
    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console.Console(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console.Console(constants['screen_width'], constants['panel_height'])
    
    player = None
    entities = []
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
            main_menu(con, main_menu_background_image, constants['screen_width'],
                      constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                if not game_options(constants) == "nah":
                    player, entities, game_map, message_log, game_state = get_game_variables(constants, names_list, colors_list)
                    game_state = GameStates.PLAYERS_TURN

                    show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)
            play_game(player, entities, game_map, message_log, game_state, con, panel, constants, names_list, colors_list)

            show_main_menu = True


if __name__ == '__main__':
    main()
