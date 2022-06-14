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

    # Note: I'm sorry in advanced. 

    try: #retrieve current high score data
        with shelve.open('scoreboard', 'c') as current_score_data:
            current_comparison_score_one = current_score_data['player_score_one']
            current_comparison_score_two = current_score_data['player_score_two']
            current_comparison_score_three = current_score_data['player_score_three']
            current_comparison_score_four = current_score_data['player_score_four']
            current_comparison_score_five = current_score_data['player_score_five']
            
            current_comparison_name_one = current_score_data['player_name_one']
            current_comparison_name_two = current_score_data['player_name_two']
            current_comparison_name_three = current_score_data['player_name_three']
            current_comparison_name_four = current_score_data['player_name_four']
            current_comparison_name_five = current_score_data['player_name_five']
    except: #if that fails write a new 'scoreboard.dat' & assign all the components a value of 0.
        initialize_high_scores()
        
        current_comparison_score_one = 0
        current_comparison_score_two = 0
        current_comparison_score_three = 0
        current_comparison_score_four = 0
        current_comparison_score_five = 0

    #player beat rank 1
    if current_comparison_score_one < player_score and current_comparison_score_one != player_name: 
        with shelve.open('scoreboard', 'c') as new_final_data:
            #four is five
            new_final_data['player_name_five'] = new_final_data['player_name_four']
            new_final_data['player_score_five'] = new_final_data['player_score_four']
            new_final_data['player_class_five'] = new_final_data['player_class_four']
            new_final_data['player_level_five'] = new_final_data['player_level_four']
            new_final_data['dungeon_level_five'] = new_final_data['dungeon_level_four']
            #three is four
            new_final_data['player_name_four'] = new_final_data['player_name_three']
            new_final_data['player_score_four'] = new_final_data['player_score_three']
            new_final_data['player_class_four'] = new_final_data['player_class_three']
            new_final_data['player_level_four'] = new_final_data['player_level_three']
            new_final_data['dungeon_level_four'] = new_final_data['dungeon_level_three']
            #two is three
            new_final_data['player_name_three'] = new_final_data['player_name_two']
            new_final_data['player_score_three'] = new_final_data['player_score_two']
            new_final_data['player_class_three'] = new_final_data['player_class_two']
            new_final_data['player_level_three'] = new_final_data['player_level_two']
            new_final_data['dungeon_level_three'] = new_final_data['dungeon_level_two']
            #one is two
            new_final_data['player_name_two'] = new_final_data['player_name_one']
            new_final_data['player_score_two'] = new_final_data['player_score_one']
            new_final_data['player_class_two'] = new_final_data['player_class_one']
            new_final_data['player_level_two'] = new_final_data['player_level_one']
            new_final_data['dungeon_level_two'] = new_final_data['dungeon_level_one']
            #player's score is one
            new_final_data['player_name_one'] = player_name
            new_final_data['player_score_one'] = player_score
            new_final_data['player_class_one'] = player_class
            new_final_data['player_level_one'] = player_level
            new_final_data['dungeon_level_one'] = dungeon_level

    #player beat rank 2
    elif current_comparison_score_two < player_score and player_score < current_comparison_score_one and current_comparison_score_two != player_name: 
        with shelve.open('scoreboard', 'c') as new_final_data:
            #four is five
            new_final_data['player_name_five'] = new_final_data['player_name_four']
            new_final_data['player_score_five'] = new_final_data['player_score_four']
            new_final_data['player_class_five'] = new_final_data['player_class_four']
            new_final_data['player_level_five'] = new_final_data['player_level_four']
            new_final_data['dungeon_level_five'] = new_final_data['dungeon_level_four']
            #three is four
            new_final_data['player_name_four'] = new_final_data['player_name_three']
            new_final_data['player_score_four'] = new_final_data['player_score_three']
            new_final_data['player_class_four'] = new_final_data['player_class_three']
            new_final_data['player_level_four'] = new_final_data['player_level_three']
            new_final_data['dungeon_level_four'] = new_final_data['dungeon_level_three']
            #two is three
            new_final_data['player_name_three'] = new_final_data['player_name_two']
            new_final_data['player_score_three'] = new_final_data['player_score_two']
            new_final_data['player_class_three'] = new_final_data['player_class_two']
            new_final_data['player_level_three'] = new_final_data['player_level_two']
            new_final_data['dungeon_level_three'] = new_final_data['dungeon_level_two']
            #player's score is two
            new_final_data['player_name_two'] = player_name
            new_final_data['player_score_two'] = player_score
            new_final_data['player_class_two'] = player_class
            new_final_data['player_level_two'] = player_level
            new_final_data['dungeon_level_two'] = dungeon_level

    #player beat rank 3
    elif current_comparison_score_three < player_score and player_score < current_comparison_score_two and current_comparison_score_three != player_name: 
        with shelve.open('scoreboard', 'c') as new_final_data:
            #four is five
            new_final_data['player_name_five'] = new_final_data['player_name_four']
            new_final_data['player_score_five'] = new_final_data['player_score_four']
            new_final_data['player_class_five'] = new_final_data['player_class_four']
            new_final_data['player_level_five'] = new_final_data['player_level_four']
            new_final_data['dungeon_level_five'] = new_final_data['dungeon_level_four']
            #three is four
            new_final_data['player_name_four'] = new_final_data['player_name_three']
            new_final_data['player_score_four'] = new_final_data['player_score_three']
            new_final_data['player_class_four'] = new_final_data['player_class_three']
            new_final_data['player_level_four'] = new_final_data['player_level_three']
            new_final_data['dungeon_level_four'] = new_final_data['dungeon_level_three']
            #player's score is three
            new_final_data['player_name_three'] = player_name
            new_final_data['player_score_three'] = player_score
            new_final_data['player_class_three'] = player_class
            new_final_data['player_level_three'] = player_level
            new_final_data['dungeon_level_three'] = dungeon_level

    #player beat rank 4
    elif current_comparison_score_four < player_score and player_score < current_comparison_score_three and current_comparison_score_four != player_name: 
        with shelve.open('scoreboard', 'c') as new_final_data:
            #four is five
            new_final_data['player_name_five'] = new_final_data['player_name_four']
            new_final_data['player_score_five'] = new_final_data['player_score_four']
            new_final_data['player_class_five'] = new_final_data['player_class_four']
            new_final_data['player_level_five'] = new_final_data['player_level_four']
            new_final_data['dungeon_level_five'] = new_final_data['dungeon_level_four']
            #Player's score is four
            new_final_data['player_name_four'] = player_name
            new_final_data['player_score_four'] = player_score
            new_final_data['player_class_four'] = player_class
            new_final_data['player_level_four'] = player_level
            new_final_data['dungeon_level_four'] = dungeon_level

    #player beat rank 5
    elif current_comparison_score_five < player_score and player_score < current_comparison_score_four and current_comparison_score_five != player_name: 
        with shelve.open('scoreboard', 'c') as new_final_data:
            new_final_data['player_name_five'] = player_name
            new_final_data['player_score_five'] = player_score
            new_final_data['player_class_five'] = player_class
            new_final_data['player_level_five'] = player_level
            new_final_data['dungeon_level_five'] = dungeon_level

    else: #player didn't crack top 5
        return

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
