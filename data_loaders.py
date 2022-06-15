from asyncio import constants
from html import entities
import os
import shelve

def save_game(player, entities, game_map, message_log, game_state, constants):
    with shelve.open('savegame', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['constants'] = constants

def save_high_score(player_name, player_score, player_class, player_level, dungeon_level):

    try: #retrieve current high score data
        with shelve.open('scoreboard', 'c') as score_data:
            rank_one_name = score_data['player_name_one']
            rank_one_score = score_data['player_score_one']
            rank_one_class = score_data['player_class_one']
            rank_one_level = score_data['player_level_one']
            rank_one_dlevel = score_data['dungeon_level_one']

            rank_two_name = score_data['player_name_two']
            rank_two_score = score_data['player_score_two']
            rank_two_class = score_data['player_class_two']
            rank_two_level = score_data['player_level_two']
            rank_two_dlevel = score_data['dungeon_level_two']

            rank_three_name = score_data['player_name_three']
            rank_three_score = score_data['player_score_three']
            rank_three_class = score_data['player_class_three']
            rank_three_level = score_data['player_level_three']
            rank_three_dlevel = score_data['dungeon_level_three']

            rank_four_name = score_data['player_name_four']
            rank_four_score = score_data['player_score_four']
            rank_four_class = score_data['player_class_four']
            rank_four_level = score_data['player_level_four']
            rank_four_dlevel = score_data['dungeon_level_four']

            rank_five_name = score_data['player_name_five']
            rank_five_score = score_data['player_score_five']
            rank_five_class = score_data['player_class_five']
            rank_five_level = score_data['player_level_five']
            rank_five_dlevel = score_data['dungeon_level_five']

    except: #if that fails write a new 'scoreboard.dat' & assign all the components a value of 0.
        initialize_high_scores()

        rank_one_name = 0
        rank_one_score = 0
        rank_one_class = 0
        rank_one_level = 0
        rank_one_dlevel = 0

        rank_two_name = 0
        rank_two_score = 0
        rank_two_class = 0
        rank_two_level = 0
        rank_two_dlevel = 0

        rank_three_name = 0 
        rank_three_score = 0
        rank_three_class = 0
        rank_three_level = 0
        rank_three_dlevel = 0

        rank_four_name = 0
        rank_four_score = 0
        rank_four_class = 0
        rank_four_level = 0
        rank_four_dlevel = 0

        rank_five_name = 0
        rank_five_score = 0
        rank_five_class = 0
        rank_five_level = 0
        rank_five_dlevel = 0

    #list's a bit messy, but you get the picture. put each rank's values in a list, put each aforementioned list in a list
    score_list = [(rank_one_name, rank_one_score, rank_one_class, rank_one_level, rank_one_dlevel),
                  (rank_two_name, rank_two_score, rank_two_class, rank_two_level, rank_two_dlevel), 
                  (rank_three_name, rank_three_score, rank_three_class, rank_three_level, rank_three_dlevel), 
                  (rank_four_name, rank_four_score, rank_four_class, rank_four_level, rank_four_dlevel), 
                  (rank_five_name, rank_five_score, rank_five_class, rank_five_level, rank_five_dlevel), 
                  (player_name, player_score, player_class, player_level, dungeon_level)]

    #sort list by value of second parameter (player score)
    score_list.sort(key=lambda a: a[1], reverse=True) 

    #save the new scoreboard
    with shelve.open('scoreboard', 'c') as final_scores:
        final_scores['player_name_one'] = score_list[0][0]
        final_scores['player_score_one'] = score_list[0][1]
        final_scores['player_class_one'] = score_list[0][2]
        final_scores['player_level_one'] = score_list[0][3]
        final_scores['dungeon_level_one'] = score_list[0][4]
        
        final_scores['player_name_two'] = score_list[1][0]
        final_scores['player_score_two'] = score_list[1][1]
        final_scores['player_class_two'] = score_list[1][2]
        final_scores['player_level_two'] = score_list[1][3]
        final_scores['dungeon_level_two'] = score_list[1][4]
        
        final_scores['player_name_three'] = score_list[2][0]
        final_scores['player_score_three'] = score_list[2][1]
        final_scores['player_class_three'] = score_list[2][2]
        final_scores['player_level_three'] = score_list[2][3]
        final_scores['dungeon_level_three'] = score_list[2][4]
        
        final_scores['player_name_four'] = score_list[3][0]
        final_scores['player_score_four'] = score_list[3][1]
        final_scores['player_class_four'] = score_list[3][2]
        final_scores['player_level_four'] = score_list[3][3]
        final_scores['dungeon_level_four'] = score_list[3][4]
        
        final_scores['player_name_five'] = score_list[4][0]
        final_scores['player_score_five'] = score_list[4][1]
        final_scores['player_class_five'] = score_list[4][2]
        final_scores['player_level_five'] = score_list[4][3]
        final_scores['dungeon_level_five'] = score_list[4][4]

#Oh No! Our handy-dandy scoreboard.dat doesn't exist or needs erased for whatever particular reason! 
#Good thing I got tired of deleting it myself and wrote this handy function!
def initialize_high_scores(): 
    with shelve.open('scoreboard', 'n') as new_scores_file:
        new_scores_file['player_name_one'] = 0
        new_scores_file['player_score_one'] = 0
        new_scores_file['player_class_one'] = 0
        new_scores_file['player_level_one'] = 0
        new_scores_file['dungeon_level_one'] = 0
        new_scores_file['player_name_two'] = 0
        new_scores_file['player_score_two'] = 0
        new_scores_file['player_class_two'] = 0
        new_scores_file['player_level_two'] = 0
        new_scores_file['dungeon_level_two'] = 0
        new_scores_file['player_name_three'] = 0
        new_scores_file['player_score_three'] = 0
        new_scores_file['player_class_three'] = 0
        new_scores_file['player_level_three'] = 0
        new_scores_file['dungeon_level_three'] = 0
        new_scores_file['player_name_four'] = 0
        new_scores_file['player_score_four'] = 0
        new_scores_file['player_class_four'] = 0
        new_scores_file['player_level_four'] = 0
        new_scores_file['dungeon_level_four'] = 0
        new_scores_file['player_name_five'] = 0
        new_scores_file['player_score_five'] = 0
        new_scores_file['player_class_five'] = 0
        new_scores_file['player_level_five'] = 0
        new_scores_file['dungeon_level_five'] = 0
        new_scores_file['tuple_buffer_one'] = 0

def load_high_scores():
    if not os.path.isfile('scoreboard.dat'):
        initialize_high_scores()

    with shelve.open('scoreboard', 'r') as score_data: 
        player_one = score_data['player_name_one']
        player_score_one = score_data['player_score_one']
        player_class_one = score_data['player_class_one']
        player_level_one = score_data['player_level_one']
        dungeon_level_one = score_data['dungeon_level_one']
        player_two = score_data['player_name_two']
        player_score_two = score_data['player_score_two']
        player_class_two = score_data['player_class_two']
        player_level_two = score_data['player_level_two']
        dungeon_level_two = score_data['dungeon_level_two']
        player_three = score_data['player_name_three']
        player_score_three = score_data['player_score_three']
        player_class_three = score_data['player_class_three']
        player_level_three = score_data['player_level_three']
        dungeon_level_three = score_data['dungeon_level_three']
        player_four = score_data['player_name_four']
        player_score_four = score_data['player_score_four']
        player_class_four = score_data['player_class_four']
        player_level_four = score_data['player_level_four']
        dungeon_level_four = score_data['dungeon_level_four']
        player_five = score_data['player_name_five']
        player_score_five = score_data['player_score_five']
        player_class_five = score_data['player_class_five']
        player_level_five = score_data['player_level_five']
        dungeon_level_five = score_data['dungeon_level_five']

    #Indented & parenthasese'd(?) for the sake of readability
    return (player_one, player_score_one, player_class_one, player_level_one, dungeon_level_one, 
    player_two, player_score_two, player_class_two, player_level_two, dungeon_level_two, 
    player_three, player_score_three, player_class_three, player_level_three, dungeon_level_three, 
    player_four, player_score_four, player_class_four, player_level_four, dungeon_level_four, 
    player_five, player_score_five, player_class_five, player_level_five, dungeon_level_five)

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

    return player, entities, game_map, message_log, game_state, constants
