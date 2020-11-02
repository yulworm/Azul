import numpy as np
import Azul_game
#from tile_factory import tile_factory
#from player_mat import player_mat

class ai_random(object):
    """description of class"""

    def __init__(self, use_tactics=True):
        self.use_tactics = use_tactics

    def choose_action(self, game):
        g_actions = game.available_actions(game)

        if self.use_tactics:
            # avoid putting a tile in the penalty
            rows_to_avoid = [Azul_game.penalty_stack_row_idx]

            # avoid filling a row and ending the game
            wall = game.players[game.current_player_idx].wall
            for i in range(0,5):
                if sum(wall[i]) == 4:
                    rows_to_avoid.append(i)

            for row in rows_to_avoid:
                f_actions = list()
                for action in g_actions:
                    if action[2]!=row:
                        f_actions.append(action)

                # if there are still any actions left, then we will use the filtered list
                if len(f_actions) > 0:
                    g_actions = f_actions

        return g_actions[np.random.choice(len(g_actions))]
    
    def get_name(self):
        return f"random_ai_{self.use_tactics}"