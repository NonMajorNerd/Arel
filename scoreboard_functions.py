import os
from random import randint
import shelve

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
            rank_six_name = score_data['player_name_six']
            rank_six_score = score_data['player_score_six']
            rank_six_class = score_data['player_class_six']
            rank_six_level = score_data['player_level_six']
            rank_six_dlevel = score_data['dungeon_level_six']
            rank_seven_name = score_data['player_name_seven']
            rank_seven_score = score_data['player_score_seven']
            rank_seven_class = score_data['player_class_seven']
            rank_seven_level = score_data['player_level_seven']
            rank_seven_dlevel = score_data['dungeon_level_seven']
            rank_eight_name = score_data['player_name_eight']
            rank_eight_score = score_data['player_score_eight']
            rank_eight_class = score_data['player_class_eight']
            rank_eight_level = score_data['player_level_eight']
            rank_eight_dlevel = score_data['dungeon_level_eight']
            rank_nine_name = score_data['player_name_nine']
            rank_nine_score = score_data['player_score_nine']
            rank_nine_class = score_data['player_class_nine']
            rank_nine_level = score_data['player_level_nine']
            rank_nine_dlevel = score_data['dungeon_level_nine']
            rank_ten_name = score_data['player_name_ten']
            rank_ten_score = score_data['player_score_ten']
            rank_ten_class = score_data['player_class_ten']
            rank_ten_level = score_data['player_level_ten']
            rank_ten_dlevel = score_data['dungeon_level_ten']

    except: #if that fails write a new 'scoreboard.dat' & assign all the components a value of 0.
        initialize_high_scores()

        #assigning an assload of variables gets irritating, n I like my scripts to pretend to be organized
        rank_one_name = 0; rank_one_score = 0; rank_one_class = 0; rank_one_level = 0; rank_one_dlevel = 0
        rank_two_name = 0; rank_two_score = 0; rank_two_class = 0; rank_two_level = 0; rank_two_dlevel = 0
        rank_three_name = 0; rank_three_score = 0; rank_three_class = 0; rank_three_level = 0; rank_three_dlevel = 0
        rank_four_name = 0; rank_four_score = 0; rank_four_class = 0; rank_four_level = 0; rank_four_dlevel = 0
        rank_five_name = 0; rank_five_score = 0; rank_five_class = 0; rank_five_level = 0; rank_five_dlevel = 0
        rank_six_name = 0; rank_six_score = 0; rank_six_class = 0; rank_six_level = 0; rank_six_dlevel = 0
        rank_seven_name = 0; rank_seven_score = 0; rank_seven_class = 0; rank_seven_level = 0; rank_seven_dlevel = 0
        rank_eight_name = 0; rank_eight_score = 0; rank_eight_class = 0; rank_eight_level = 0; rank_eight_dlevel = 0
        rank_nine_name = 0; rank_nine_score = 0; rank_nine_class = 0; rank_nine_level = 0; rank_nine_dlevel = 0
        rank_ten_name = 0; rank_ten_score = 0; rank_ten_class = 0; rank_ten_level = 0; rank_ten_dlevel = 0

    #list's a bit messy, but you get the picture. put each rank's values in a list, put each aforementioned list in a list
    score_list = [(rank_one_name, rank_one_score, rank_one_class, rank_one_level, rank_one_dlevel),
                  (rank_two_name, rank_two_score, rank_two_class, rank_two_level, rank_two_dlevel), 
                  (rank_three_name, rank_three_score, rank_three_class, rank_three_level, rank_three_dlevel), 
                  (rank_four_name, rank_four_score, rank_four_class, rank_four_level, rank_four_dlevel), 
                  (rank_five_name, rank_five_score, rank_five_class, rank_five_level, rank_five_dlevel),
                  (rank_six_name, rank_six_score, rank_six_class, rank_six_level, rank_six_dlevel), 
                  (rank_seven_name, rank_seven_score, rank_seven_class, rank_seven_level, rank_seven_dlevel), 
                  (rank_eight_name, rank_eight_score, rank_eight_class, rank_eight_level, rank_eight_dlevel), 
                  (rank_nine_name, rank_nine_score, rank_nine_class, rank_nine_level, rank_nine_dlevel), 
                  (rank_ten_name, rank_ten_score, rank_ten_class, rank_ten_level, rank_ten_dlevel), 
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
        final_scores['player_name_six'] = score_list[5][0]
        final_scores['player_score_six'] = score_list[5][1]
        final_scores['player_class_six'] = score_list[5][2]
        final_scores['player_level_six'] = score_list[5][3]
        final_scores['dungeon_level_six'] = score_list[5][4]
        final_scores['player_name_seven'] = score_list[6][0]
        final_scores['player_score_seven'] = score_list[6][1]
        final_scores['player_class_seven'] = score_list[6][2]
        final_scores['player_level_seven'] = score_list[6][3]
        final_scores['dungeon_level_seven'] = score_list[6][4]
        final_scores['player_name_eight'] = score_list[7][0]
        final_scores['player_score_eight'] = score_list[7][1]
        final_scores['player_class_eight'] = score_list[7][2]
        final_scores['player_level_eight'] = score_list[7][3]
        final_scores['dungeon_level_eight'] = score_list[7][4]
        final_scores['player_name_nine'] = score_list[8][0]
        final_scores['player_score_nine'] = score_list[8][1]
        final_scores['player_class_nine'] = score_list[8][2]
        final_scores['player_level_nine'] = score_list[8][3]
        final_scores['dungeon_level_nine'] = score_list[8][4]
        final_scores['player_name_ten'] = score_list[9][0]
        final_scores['player_score_ten'] = score_list[9][1]
        final_scores['player_class_ten'] = score_list[9][2]
        final_scores['player_level_ten'] = score_list[9][3]
        final_scores['dungeon_level_ten'] = score_list[9][4]

#randomize the high score table upon first start-up to fill the space, give the player a goal to reach, a one-sided rivalry
def initialize_high_scores(): 

    player_one = ['Marble', randint(1, 100), 'Tourist', randint(1, 10), randint(1,25)]
    player_two = ['Taco', randint(1, 100), 'Adventurer', randint(1, 10), randint(1,25)]
    player_three = ['Rosemary', randint(1, 100), 'Merchant', randint(1, 10), randint(1,25)]
    player_four = ['Soybean', randint(1, 100), 'Criminal', randint(1, 10), randint(1,25)]
    player_five = ['Juniper', randint(1, 100), 'Ranger', randint(1, 10), randint(1,25)]
    player_six = ['Default Dan', randint(1, 100), 'Adventurer', randint(1, 10), randint(1,25)]
    player_seven = ['Beans', randint(1, 100), 'Criminal', randint(1, 10), randint(1,25)]
    player_eight = ['Your Mother', randint(1, 100), 'Tourist', randint(1, 10), randint(1,25)]
    player_nine = ['Charlie', randint(1, 100), 'Ranger', randint(1, 10), randint(1,25)]
    player_ten = ['Towlie', randint(1, 100), 'Merchant', randint(1, 10), randint(1,25)]

    score_list = [(player_one), (player_two), (player_three), (player_four), (player_five), (player_six), (player_seven), (player_eight), (player_nine), (player_ten)]
     
    score_list.sort(key=lambda a: a[1], reverse = True)
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
        final_scores['player_name_six'] = score_list[5][0]
        final_scores['player_score_six'] = score_list[5][1]
        final_scores['player_class_six'] = score_list[5][2]
        final_scores['player_level_six'] = score_list[5][3]
        final_scores['dungeon_level_six'] = score_list[5][4]
        final_scores['player_name_seven'] = score_list[6][0]
        final_scores['player_score_seven'] = score_list[6][1]
        final_scores['player_class_seven'] = score_list[6][2]
        final_scores['player_level_seven'] = score_list[6][3]
        final_scores['dungeon_level_seven'] = score_list[6][4]
        final_scores['player_name_eight'] = score_list[7][0]
        final_scores['player_score_eight'] = score_list[7][1]
        final_scores['player_class_eight'] = score_list[7][2]
        final_scores['player_level_eight'] = score_list[7][3]
        final_scores['dungeon_level_eight'] = score_list[7][4]
        final_scores['player_name_nine'] = score_list[8][0]
        final_scores['player_score_nine'] = score_list[8][1]
        final_scores['player_class_nine'] = score_list[8][2]
        final_scores['player_level_nine'] = score_list[8][3]
        final_scores['dungeon_level_nine'] = score_list[8][4]
        final_scores['player_name_ten'] = score_list[9][0]
        final_scores['player_score_ten'] = score_list[9][1]
        final_scores['player_class_ten'] = score_list[9][2]
        final_scores['player_level_ten'] = score_list[9][3]
        final_scores['dungeon_level_ten'] = score_list[9][4]

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
        player_six = score_data['player_name_six']
        player_score_six = score_data['player_score_six']
        player_class_six = score_data['player_class_six']
        player_level_six = score_data['player_level_six']
        dungeon_level_six = score_data['dungeon_level_six']
        player_seven = score_data['player_name_seven']
        player_score_seven = score_data['player_score_seven']
        player_class_seven = score_data['player_class_seven']
        player_level_seven = score_data['player_level_seven']
        dungeon_level_seven = score_data['dungeon_level_seven']
        player_eight = score_data['player_name_eight']
        player_score_eight = score_data['player_score_eight']
        player_class_eight = score_data['player_class_eight']
        player_level_eight = score_data['player_level_eight']
        dungeon_level_eight = score_data['dungeon_level_eight']
        player_nine = score_data['player_name_nine']
        player_score_nine = score_data['player_score_nine']
        player_class_nine = score_data['player_class_nine']
        player_level_nine = score_data['player_level_nine']
        dungeon_level_nine = score_data['dungeon_level_nine']
        player_ten = score_data['player_name_ten']
        player_score_ten = score_data['player_score_ten']
        player_class_ten = score_data['player_class_ten']
        player_level_ten = score_data['player_level_ten']
        dungeon_level_ten = score_data['dungeon_level_ten']

    #Indented & parenthasese'd(?) for the sake of readability
    return (player_one, player_score_one, player_class_one, player_level_one, dungeon_level_one, 
    player_two, player_score_two, player_class_two, player_level_two, dungeon_level_two, 
    player_three, player_score_three, player_class_three, player_level_three, dungeon_level_three, 
    player_four, player_score_four, player_class_four, player_level_four, dungeon_level_four, 
    player_five, player_score_five, player_class_five, player_level_five, dungeon_level_five,
    player_six, player_score_six, player_class_six, player_level_six, dungeon_level_six, 
    player_seven, player_score_seven, player_class_seven, player_level_seven, dungeon_level_seven, 
    player_eight, player_score_eight, player_class_eight, player_level_eight, dungeon_level_eight, 
    player_nine, player_score_nine, player_class_nine, player_level_nine, dungeon_level_nine, 
    player_ten, player_score_ten, player_class_ten, player_level_ten, dungeon_level_ten)