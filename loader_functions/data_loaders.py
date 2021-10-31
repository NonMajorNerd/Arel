import os
import shelve
import _globals
def save_game(player, game_map, message_log, game_state):
    print(str(_globals.entities.index(player)))
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = _globals.entities.index(player)
        data_file['entities'] = _globals.entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['constants'] = _globals.constants


def load_game():
    if not os.path.isfile('savegame.dat'):
        raise FileNotFoundError

    with shelve.open('savegame', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        constants = data_file['constants']
        
    player = entities[player_index]

    return player, game_map, message_log, game_state
