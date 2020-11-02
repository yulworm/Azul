from ai_random import ai_random
import ai_q
import play_dueling_ai
import Azul_game
import csv
import pickle
import sys
import copy
import os
import datetime
import ai_nn
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def main():
    ai = train_ai(ai_nn.ai('F5x5',True), games_folder='data', nbr_new_games=500, interesting_cut_off=60)

    results = dueling_ai([ai, ai],nbr_matches=100)
    for r in results:
        print(r)

    save_results(results)

def holding():

    filter_training_matches('data', 'x')

    dueling_ai([ai_random(), ai_random(False)],nbr_matches=100)
    #generate_random_matches(200,70)
    #ai = train_ai(ai_q.ai_q(), games_folder='data', nbr_new_games=0)

def train_ai(ai, nbr_new_games=0, games_folder=None, interesting_cut_off=50):

    if games_folder is not None:
        ai.train_from_games( read_training_matches(games_folder) )

    if nbr_new_games > 0:
        ai = generate_save_training_matches_and_train_model(ai,f'{ai.get_name()}',nbr_new_games,interesting_cut_off,games_folder)

    return ai

def save_results(results):
    filename = f'{results[0][1]}_VS_{results[0][3]}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}.csv'

    fields = ['duel_nbr', 'AI_0_name', 'AI_0_score', 'AI_1_name', 'AI_1_score', 'nbr_turns']

    with open(os.path.join('results',filename), 'w', newline='') as f: 
      
        # using csv.writer method from CSV package 
        write = csv.writer(f) 
      
        write.writerow(fields) 
        write.writerows(results) 

    plot_results(results, filename)

def plot_results(results, filename=None):
    rd = {'AI_0_score':list(), 'AI_1_score':list(), 'nbr_turns':list(), 'max_score':list(), 'min_score':list()}
    for r in results:
        rd['AI_0_score'].append(r[2])
        rd['AI_1_score'].append(r[4])
        rd['nbr_turns'].append(r[5])
        rd['max_score'].append(max(r[2],r[4]))
        rd['min_score'].append(min(r[2],r[4]))

    #df = pd.DataFrame(scores_for_df, columns=[results[0][1], results[0][3]])
    df = pd.DataFrame(rd)

    # bubble https://seaborn.pydata.org/examples/scatter_bubbles.html
#    bubble = df.groupby(['nbr_turns','max_score']).agg(np.size)

    #sns.set(rc={'figure.figsize':(2,2)})
    

    fig, (ax1, ax2) = plt.subplots(1,2, figsize = (12, 5))

    ax1.boxplot(df[['AI_0_score','AI_1_score']], labels=[results[0][1], results[0][3]])
    ax1.grid()

    ax2.scatter(df.nbr_turns,df.max_score)
    ax2.grid()

    #plt.show(block=True)
    if filename is not None:
        plt.savefig(os.path.join('results',filename.replace('.csv','.png')))
    else:
        plt.show()

def play_randoms():
    ais = [ai_random(), ai_random()]

    results = dueling_ai(ais,100)
    for r in results:
        print(r)

def dueling_ai(ais, nbr_matches=100):
    results = list()
    player_0_wins = 0
    for i in range(0,nbr_matches):

        game = Azul_game.Azul_game()
        nbr_turns = 0
        while game.winner is None:
            action = ais[game.current_player_idx].choose_action(game)

            game.move( action )
            nbr_turns += 1
    
        results.append((i, ais[0].get_name(), game.players[0].get_total_score(), ais[1].get_name(), game.players[1].get_total_score(), nbr_turns))

        if game.players[0].get_total_score() > game.players[1].get_total_score():
            player_0_wins += 1

        progress(i, nbr_matches)
    sys.stdout.write('\n')

    print(f'Player 0 won {100 * player_0_wins / nbr_matches}% of matches')

    return results

def generate_save_training_matches_and_train_model(ai, save_name, nbr_interesting_saves, interesting_score, folder_location):
    saves_per_file = 100
    saves_remaining = nbr_interesting_saves
    while saves_remaining > 0:
        ai.train_from_games( generate_and_save_training_matches([ai, ai],save_name, min(saves_per_file, saves_remaining), interesting_score, folder_location) )
        saves_remaining -= min(saves_per_file, saves_remaining)
    return ai

def generate_random_matches(nbr_interesting_saves,interesting_score=50):
    ais = [ai_random(), ai_random()]
    saves_per_file = 100
    saves_remaining = nbr_interesting_saves
    while saves_remaining > 0:
        generate_and_save_training_matches(ais,f'random',min(saves_per_file, saves_remaining),interesting_score,'data')
        saves_remaining -= min(saves_per_file, saves_remaining)

def generate_and_save_training_matches(ais, save_name, nbr_interesting_saves, interesting_score, folder_location):

    saved_games = list()
    results = list()
    games_played = 0
    while nbr_interesting_saves > len(saved_games):

        progress(len(saved_games), nbr_interesting_saves, games_played)
        game = Azul_game.Azul_game()

        # we store the sequence of turn for each player separately, that way I can save them separately if only one of them is interesting
        game_sequence = [list(), list()]
        nbr_turns = 0
        score_dropped = [False, False]
        while game.winner is None:
            player = game.current_player_idx
            start_state = copy.deepcopy(game)
            action = ais[player].choose_action(game)
            game.move( action )

            game_sequence[player].append( (start_state, action, copy.deepcopy(game)) )

            # we are not interested in games where the player's scrore decreased at any time, that means they did something wrong
            score_dropped[player] = score_dropped[player] or start_state.players[player].cummulative_score > game.players[player].cummulative_score

            nbr_turns += 1

        games_played += 1
        for player in range(0,1):
            # if the score of the last moved played by a player is greater than the treashold, then we save it
            if game_sequence[player][-1][2].players[player].get_total_score() > interesting_score and not score_dropped[player]:
                saved_games.append(game_sequence[player])

                results.append((save_name, len(saved_games), game_sequence[player][-1][2].players[player].get_total_score(), len(game_sequence[player])))

    sys.stdout.write('\n')

    with open(os.path.join(folder_location,f'{save_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}_{nbr_interesting_saves}_matches_min_{interesting_score}.azgd'), 'wb') as match_file:
        
      pickle.dump(saved_games, match_file)
      print(os.path.abspath(match_file.name))

    return saved_games

def read_training_matches(folder_location, approx_max_nbr_games=-1):
    games = list()

    for f in os.listdir(folder_location):
        print(f)
        #if not os.path.isfile(f):
        #    continue
        if approx_max_nbr_games != -1 and len(games) >= approx_max_nbr_games:
            break

        with open( os.path.join(folder_location,f), 'rb' ) as match_file:
            games.extend( pickle.load(match_file) )

    return games

def filter_training_matches(old_folder,new_folder):
    tranches = dict()
    for i in range(5,20):
        tranches[i] = list()

    nbr_rejected = 0
    for game_sequence in read_training_matches(old_folder):
        score_dropped = False
        used_penatly = False
        final_score = 0
        for f_game, g_action, t_game in game_sequence:        
            player = f_game.current_player_idx
            score_dropped = f_game.players[player].cummulative_score > t_game.players[player].cummulative_score
            used_penalty = g_action[2] == Azul_game.penalty_stack_row_idx
            if score_dropped or used_penalty:
                break
            final_score = t_game.players[player].get_total_score()
        # is there a reason to ignore this game sequence?
        if score_dropped or used_penalty:
            nbr_rejected += 1
            continue

        tranches[final_score//10].append(game_sequence)

    print(f'{nbr_rejected} games rejected')

    for i, games in tranches.items():
        range_desc = f'{i*10}_{(i+1)*10-1}'
        if len(games) > 0:
            with open(os.path.join(new_folder,f'filtered_{datetime.datetime.now().strftime("%Y%m%d_%H%M")}_{len(games)}_matches_{range_desc}.azgd'), 'wb') as match_file:
              pickle.dump(games, match_file)
              print(os.path.abspath(match_file.name))
        else:
            print(f'Nothing for {range_desc}')


def progress(count, total, status=''):
    """
    From https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

if __name__ == "__main__":
    main()