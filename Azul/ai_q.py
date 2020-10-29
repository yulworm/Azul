import copy
import sys
import numpy as np
import random
from Azul_game import Azul_game
from tile_factory import tile_factory
from player_mat import player_mat
import ai_random

class ai_q(object):
    """description of class"""
    debug = False

    def __init__(self, alpha=0.5, epsilon=0.1, use_epsilon=False):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.
        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of remaining piles, e.g. (1, 1, 4, 4)
         - `action` is a tuple `(i, j)` for an action
        """
        self.q = dict()
        self.alpha = alpha
        self.epsilon = epsilon
        self.use_epsilon = use_epsilon
        self.ai_random = ai_random.ai_random()

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """
        return self.q.get((state, action),0)

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.
        Use the formula:
        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)
        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """
        self.q[(state, action)] = old_q + self.alpha * ((reward + future_rewards)  - old_q)

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.
        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """
        b_a, b_q = self.best_action_with_value(state)
        if b_a is None:
            return 0
        else:
            return b_q

    def best_action_with_value(self, state):
        # get all the possible actions given the state
        # at most there can be 15 tiles of a type that can be moved
        actions = list()
        for tt in range(0,5):
            for i in range(1,6): # theoretically this can go up to 15, but that is too much variability for us to handle
                for row in range(0,6):
                    actions.append((tt,i,row))

        return self.best_action_with_value_given_limited_actions(state, actions)

    def best_action_with_value_given_limited_actions(self, state, actions):
        """
        returns a tuple (action, value), where action is a tuple and value is the expected reward for taking that action
        if there are no calculated values for any of the possible actions, then the first action is returned with a value of 0
        """
        b_q = -2
        b_a = None

        for a in actions:
            q = self.get_q_value(state, a)

            if q > b_q:
                b_q = q
                b_a = a

        if b_q == 0:
            return (None, None)
        else:
            return (b_a, b_q)


    def choose_q_action(self, state, actions):
        if self.use_epsilon and random.choices([True,False], [self.epsilon,(1-self.epsilon)]):
            return random.choice(actions)
        else:
            a, q = self.best_action_with_value_given_limited_actions(state, actions)
            if self.debug:
                print(f'{a} - {q}')
            return a

    def choose_action(self, game):
        """
        Given a game, return an action `(tile_type, from_pile, to_stack, nbr_to_move)` to take.
        The state we use to calculate the q value is a small subset of the actual game state, so there is a good bit of logic
        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).
        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.
        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        # the state is the current player's wall and floor
        q_state = get_state_for_game(game, game.current_player_idx)
        g_actions = game.available_actions(game)
        q_actions = get_get_q_actions_from_game_actions(g_actions)

        q_action = self.choose_q_action(q_state, q_actions)

        # if the q algo has no real insight, just pick using the semi random method
        if q_action is None:
            return self.ai_random.choose_action(game)

        from_piles = set()
        for tile_type, from_pile, to_stack, nbr_to_move in g_actions:
            if q_action[0] == tile_type and q_action[1] == nbr_to_move and q_action[2] == to_stack:
                from_piles.add(from_pile)

        # if the centre pile still has the penalty tile, then avoid the centre pile if possible
        #if game.factory.is_penalty_tile_in_centre() and len(from_piles) > 1:
        #    from_piles.remove(0)

        # tile_type, from_pile, to_stack, nbr_to_move
        return (q_action[0], np.random.choice(list(from_piles)), q_action[2], q_action[1])

    def get_name(self):
        return "q_ai_1"

def get_state_for_game(game, player):
    """
    converts the game into a simplified view that we can use for calculating q over a reasonable space
    space = (2^4)^5 * 2 * 3 * 4 * 5 = ~126 million
    """
    row_tuples = list()
    for row in game.players[player].get_merged_wall_and_floor():
        row_tuples.append(tuple(row))

    # TODO: consider adding the last round flag

    return tuple(row_tuples)

def get_get_q_actions_from_game_actions(g_actions):
    """
    The q action is a simplified version of the game actions, only containing the tile type and the number of tiles to move
    Action is a tuple tile_type,nbr_to_move
    """
    q_actions = set()
    for ga in g_actions:
        q_actions.add( convert_game_action_to_q_action(ga) )

    return list(q_actions)

def convert_game_action_to_q_action(g_action):
    return (g_action[0],g_action[3],g_action[2])

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

def train_from_self(n, ai=None):
    """
    Train an AI by playing `n` games against itself.
    """
    q_ai = ai_q()
    player_ai = ai
    if player_ai is None:
        player_ai = q_ai

    print('Training')
    # Play n games
    for i in range(n):
        if i % 500 == 0:
            print(f"Played {i} training games")
        progress(i%500, 500)
        game = Azul_game()

        # keep track of all the moved
        # {"f_state": None, "action": None, "t_state": None}
        prev = list()

        # Game loop
        while True:

            player = game.current_player_idx

            # Keep track of the state before making a move
            f_state = get_state_for_game(game, player)

            # choose an action
            g_action = player_ai.choose_action(game)
            q_action = convert_game_action_to_q_action( g_action )

            # Make move
            game.move(g_action)

            t_state = get_state_for_game(game, player)

            # When game is over, update Q values with rewards
            # the reward is equal to the score divided by 100, so it will likely be less than 1 but could be more
            # both the winner and looser get a similar reward
            if game.winner is not None:
                q_ai.update(f_state, q_action, t_state, game.players[player].get_total_score()/100)
                
                # no record the last turn of the opponent
                f_state, q_action, t_state = prev.pop()
                q_ai.update(f_state, q_action, t_state, game.players[game.other_player(player)].get_total_score()/100)

                break

            # If game is continuing, no rewards yet
            else:
                prev.append( (f_state, q_action, t_state) )

        # now replay in reverse order all of the steps to back propogate the scores
        for f_state, q_action, t_state in reversed(prev):
            q_ai.update(f_state, q_action, t_state, 0)

    print("Done training")

    # Return the trained AI
    return q_ai

def train_from_games(games, ai=None):
    q_ai = ai
    if q_ai is None:
        q_ai = ai_q()

    for game_sequence in games:
        for f_game, g_action, t_game in reversed(game_sequence):
            player = f_game.current_player_idx
            f_state = get_state_for_game(f_game, player)
            q_action = convert_game_action_to_q_action(g_action)
            t_state = get_state_for_game(t_game, player)

            q_ai.update(f_state, q_action, t_state, 0)

    return q_ai
