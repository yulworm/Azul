from tile_factory import tile_factory
from player_mat import player_mat
from Azul_game import Azul_game
import copy
import sys

def play(ais, nbr_matches, duel_name, interesting_score=-1):

    results = list()
    for i in range(0,nbr_matches):

        progress(i, nbr_matches)
        game = Azul_game()

        game_sequence = list()
        nbr_turns = 0
        while game.winner is None:
            action = ais[game.current_player_idx].choose_action(game)

            game_sequence.append( (copy.deepcopy(game), action) )

            game.move( action )
            nbr_turns += 1
    
        results.append((duel_name, i, ais[0].get_name(), game.players[0].get_total_score(), ais[1].get_name(), game.players[1].get_total_score(), nbr_turns))

        # we want to only use good examples to train an ai
        if interesting_score > -1 and game.players[0].get_total_score() > interesting_score and game.players[0].get_total_score() > interesting_score:
            # save the match to a file
            game_sequence

    return results

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

