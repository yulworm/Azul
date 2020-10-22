from tile_factory import tile_factory
from player_mat import player_mat

def main():
    game = Azul_game()

    print(game.factory)
    
    print(f'Player {game.player}')
    print(game.players[game.player])

    print(game.available_actions(game.factory, game.players[game.player]))

class Azul_game():
    """description of class"""
    def __init__(self):
        self.factory = tile_factory(6, player_mat.tile_type_order)

        self.factory.fill_factory_piles()

        self.players = [player_mat(), player_mat()]
    
        self.player = 0
        self.winner = None

    @classmethod
    def available_actions(cls, factory, mat):
        avail_actions = list()
        for tile_type in range(0,5):
            mat_rows = mat.get_rows_permitted_for_tile_type(tile_type)
            for pile_idx, t_cnt in factory.get_piles_with_tile_type(tile_type):
                for row_idx in mat_rows:
                    avail_actions.append((tile_type, pile_idx, row_idx))

        return avail_actions; 

    @classmethod
    def other_player(cls, player):
        """
        other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = Azul_game.other_player(self.player)

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be a tuple `(tile_type, from_pile, to_stack)`.
        """
        tile_type, from_pile, to_stack = action

        # Check for errors
        if self.winner is not None:
            raise Exception("Game already won")
        #elif pile < 0 or pile >= len(self.piles):
        #    raise Exception("Invalid pile")
        #elif count < 1 or count > self.piles[pile]:
        #    raise Exception("Invalid number of objects")

        # Update pile
        #self.piles[pile] -= count
        #self.switch_player()

        # Check for a winner
        if all(pile == 0 for pile in self.piles):
            self.winner = self.player

    def get_winner(self):
        return None # TODO:

    # number of tiles moved plus change in score plus change in number of completed stacks, in the case of a tie, choose randomly

if __name__ == "__main__":
    main()