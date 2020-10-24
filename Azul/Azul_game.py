from tile_factory import tile_factory
from player_mat import player_mat

def main():
    game = Azul_game()

    print(game.factory)
    
    print(f'Player {game.current_player_idx}')
    print(game.players[game.current_player_idx])

    action = game.available_actions(game.factory, game.players[game.current_player_idx])[10]
    print('--------------------------')
    print(f'making move {action}')
    print('--------------------------')
    game.move(action)
    print(game.players[game.current_player_idx])

    #game._is_coherent()

class Azul_game():
    """description of class"""
    penalty_stack_row_idx = 9
    is_last_round = False
    nbr_players = 2

    def __init__(self):
        self.factory = tile_factory(6, player_mat.tile_type_order)

        self.factory.fill_factory_piles()

        self.players = list()
        for i in range(0,self.nbr_players):
            self.players.append( player_mat() )
    
        self.current_player_idx = 0
        self.winner = None

    @classmethod
    def available_actions(cls, factory, mat):
        """
        An action consists of 3 pieces of information
        - tile type we will be moving
        - from which pile will we draw the tiles
        - to which row will we be moving the tiles
        """
        avail_actions = list()
        for tile_type in range(0,5):
            mat_rows = mat.get_rows_permitted_for_tile_type(tile_type)
            # the penalty stack is always a valid destination, we fake that with an index 
            mat_rows.append(cls.penalty_stack_row_idx)
            for pile_idx, t_cnt in factory.get_piles_with_tile_type(tile_type):
                for row_idx in mat_rows:
                    avail_actions.append((tile_type, pile_idx, row_idx))

        return avail_actions; 

#    @classmethod
#    def other_player(cls, player):
        """
        other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
#        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.current_player_idx = (self.current_player_idx + 1) // self.nbr_players

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

        # get the tiles from the factory
        nbr_tiles, penalty = self.factory.remove_tiles_from_pile(from_pile, tile_type)

        if to_stack == self.penalty_stack_row_idx:
            # these tiles are going straight to penalty
            self.players[self.current_player_idx].add_tiles_to_penalty(nbr_tiles, tile_type)
        else:
            # put the tiles on the floor
            self.players[self.current_player_idx].move_tiles_to_row(nbr_tiles, tile_type, to_stack)

        if penalty == 1:
            self.players[self.current_player_idx].add_penalty_tile_to_penalty_stack(penalty)

        # check if the round is over
        if self.factory.get_tile_count_in_piles() == 0:
            # score this round and setup the next round 
            # if the game is over, determine the winner
            if self.process_end_round():
                self.set_winner()
            # the end of round method also sets the next player
        else:
            # check if the player just did something which will end the game soon
            if not self.is_last_round:
                self.is_last_round = self.players[self.current_player_idx].has_a_completed_row()
            # pass the baton to the next player
            self.switch_player()

            

        # Update pile
        #self.piles[pile] -= count
        #self.switch_player()

        # Check for a winner
        #if all(pile == 0 for pile in self.piles):
           # self.winner = self.player

    def process_end_round(self):
        """
        Return True if the game is over
        """
        player_end_of_game = false

        # process each player
        for player in self.players:
            (ended_game, discard_tiles) = player.process_end_of_round()

            # check if they had the penalty tile
            if discard[player_mat.tile_type_order.indexOf('P')] == 1:
                # they become the current player
                self.current_player_idx = self.players.indexOf(player)

                # put the tile back in the factory
                self.factory.return_penalty_tile()

                discard[player_mat.tile_type_order.indexOf('P')] = 0

            # put the discard tiles in the factory discard
            self.factory

            if not player_end_of_game:
                player_end_of_game = ended_game

        # If none of the players ended the game and at least one tile can still be placed, then the game continues
        return player_end_of_game or factory.fill_factory_piles()

    def set_winner(self):
        """
        Returns the number of the winning player
        """
        top_score = -1
        for player in self.players:
            if player.get_total_score() > top_score:
                top_score = player.get_total_score() 
                self.winner = self.players.indexOf(player)

    def _is_coherent(self):

        # are all the tiles accounted for
        assert 201 == sum(player.get_total_tile_count() for player in self.players) + self.factory.get_total_tile_count()
if __name__ == "__main__":
    main()