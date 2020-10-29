from ai_random import ai_random
import ai_q
import play_dueling_ai
import csv

def main():
    train_q_ai_with_random()
    #play_randoms()

def train_q_ai_with_random():
    ai = ai_q.train(5000, ai_random())

    #for item in ai.q.items():
    #    print(item)

    #ai.debug = True
    ais = [ai, ai_random()]

    results = dueling_ai(ais,100,'test1')
    for r in results:
        print(r)

def play_randoms():
    ais = [ai_random(), ai_random(False)]

    results = dueling_ai(ais,100,'test1')
    for r in results:
        print(r)

def dueling_ai(ais, nbr_matches, duel_name, interesting_score=-1):

    results = list()
    interesting_matches = 0
    saved_games = list()
    while interesting_matches < nbr_matches:

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
            saved_games game_sequence
            interesting_matches += 1

        elif interesting_score == -1:
            interesting_matches += 1

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

if __name__ == "__main__":
    main()