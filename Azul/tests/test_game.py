import unittest
import numpy as np
from Azul_game import Azul_game

class Test_test_game(unittest.TestCase):
    def test_a_random_turn(self):
        game = Azul_game()

        player = game.current_player_idx
        
        actions = game.available_actions(game.factory, game.players[player])

        # make a random move
        game.move( actions[np.random.choice(len(actions))] )

        self.assertEqual(101, game.get_total_tile_count())

        # something was moved to the player's mat
        self.assertGreater(game.players[player].get_total_tile_count(), 0)

        # the current player changed so we are ready for the next move
        self.assertNotEqual(player, game.current_player_idx)

    def test_a_random_game(self):
        game = Azul_game()

        player = game.current_player_idx
        player_tile_count = 0

        actions = game.available_actions(game.factory, game.players[player])
        nbr_actions = len(actions)

        while len(actions) > 0:
            # make a random move
            game.move( actions[np.random.choice(len(actions))] )

            self.assertEqual(101, game.get_total_tile_count())

            # something was moved to the player's mat
            self.assertGreater(game.players[player].get_total_tile_count(), player_tile_count)

            player = game.current_player_idx
            player_tile_count = game.players[player].get_total_tile_count()

            actions = game.available_actions(game.factory, game.players[player])

            self.assertNotEqual(nbr_actions, len(actions))
            nbr_actions = len(actions)

if __name__ == '__main__':
    unittest.main()
