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

def main():
    #generate_random_matches(100)
    train_ai(ai_q.ai_q(), games_folder='data', nbr_new_games=200)

def train_ai(ai, nbr_new_games=0, games_folder=None, interesting_cut_off=50):

    if games_folder is not None:
        ai.train_from_games( read_training_matches(games_folder) )

    if nbr_new_games > 0:
        ai = generate_save_training_matches_and_train_model(ai,f'{ai.get_name()}',nbr_new_games,interesting_cut_off,games_folder)

    results = dueling_ai([ai, ai_random()],f'{ai.get_name()}_v_random',1000)

    return ai

def play_randoms():
    ais = [ai_random(), ai_random()]

    results = dueling_ai(ais,'test1',100)
    for r in results:
        print(r)

def dueling_ai(ais, duel_name, nbr_matches):

    results = list()
    player_0_wins = 0
    for i in range(0,nbr_matches):

        game = Azul_game.Azul_game()
        nbr_turns = 0
        while game.winner is None:
            action = ais[game.current_player_idx].choose_action(game)

            game.move( action )
            nbr_turns += 1
    
        results.append((duel_name, i, ais[0].get_name(), game.players[0].get_total_score(), ais[1].get_name(), game.players[1].get_total_score(), nbr_turns))

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
        ai.train_from_games( generate_and_save_training_matches([ai, ai],save_name, min(saves_per_file, saves_remaing), interesting_score, folder_location) )
        saves_remaining -= min(saves_per_file, saves_remaing)
    return ai

def generate_random_matches(nbr):
    ais = [ai_random(), ai_random()]
    for i in range(0,nbr//100):
        print(f'Generation loop {i}')
        generate_and_save_training_matches(ais,f'random',100,50,'data')

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
        while game.winner is None:
            player = game.current_player_idx
            start_state = copy.deepcopy(game)
            action = ais[player].choose_action(game)
            game.move( action )

            game_sequence[player].append( (start_state, action, copy.deepcopy(game)) )

            nbr_turns += 1

        games_played += 1
        for player in range(0,1):
            # if the score of the last moved played by a player is greater than the treashold, then we save it
            if game_sequence[player][-1][2].players[player].get_total_score() > interesting_score:
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