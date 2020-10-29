import numpy as np
import Azul_game
#from tile_factory import tile_factory
#from player_mat import player_mat

class ai_random(object):
    """description of class"""

    def __init__(self, exclude_penalty=True):
        self.exclude_penalty_actions = exclude_penalty

    def choose_action(self, game):
        actions = game.available_actions(game)
        action = None
        while action is None:
            action = actions[np.random.choice(len(actions))]
            if self.exclude_penalty_actions and action[2]==Azul_game.penalty_stack_row_idx: # if the action is to the discard, then skip it if you can
                for a in actions:
                    if a[2]!=Azul_game.penalty_stack_row_idx:
                        action = None
                        break

        return action

    def get_name(self):
        return "random_ai_1"