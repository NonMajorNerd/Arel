import os
import _globals
import shelve
import scoreboard_functions
from components.vendors import vendor_data_loader

def save_game(player, entities, game_map, message_log, game_state):
    with shelve.open('data_files/savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['constants'] = _globals.constants
        
    with shelve.open('data_files/vendor_data', 'n') as vendor_data:
        vendor_data['vendor_inventory'] = _globals.vendorEnt.inventory.items
        vendor_data['vendor_equipment'] = _globals.vendorEnt.equipment.list
    #also save vendor's inventory, and player's scoreboard info
    scoreboard_functions.save_high_score(_globals.constants['player_name'], player.score, _globals.constants['options_origin'], player.level.current_level, game_map.dungeon_level)

def load_game():
    if not os.path.isfile('data_files/savegame.dat'):
        raise FileNotFoundError

    with shelve.open('data_files/savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        constants = data_file['constants']
        
    with shelve.open('data_files/vendor_data', 'r') as vendor_data:
        _globals.vendorEnt.inventory.items = vendor_data['vendor_inventory']
        _globals.vendorEnt.equipment.list = vendor_data['vendor_equipment']
    
    player = entities[player_index]
    
    #also load vendor's inventory, and player's scoreboard info
    scoreboard_functions.load_high_scores()

    return player, entities, game_map, message_log, game_state, constants