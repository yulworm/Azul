import unittest
from player_mat import player_mat

class Test_test_player_mat(unittest.TestCase):
    def test_get_penalty_score_zero(self):
        mat = player_mat()
        self.assertEqual(mat.get_penalty_score(), 0)

    def test_get_penalty_score_one(self):
        mat = player_mat()
        mat.penalty_stack = [0,0,0,0,0,0,1]
        self.assertEqual(mat.get_penalty_score(), -1)

        mat.penalty_stack = [0,0,1,0,0,0,0]
        self.assertEqual(mat.get_penalty_score(), -1)

    def test_get_penalty_score_six(self):
        mat = player_mat()
        mat.penalty_stack = [0,2,0,3,0,0,1]
        self.assertEqual(mat.get_penalty_score(), -11)

        mat.penalty_stack = [4,0,1,0,0,0,1]
        self.assertEqual(mat.get_penalty_score(), -11)

    def test_set_wall_for_testing(self):
        mat = player_mat()
        mat.set_wall_for_testing([[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]])
        self.assertEqual(mat.wall,[[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1]])

    def test_get_wall_for_row_and_type(self):
        mat = player_mat()
        mat.set_wall_for_testing([[1,2,3,4,5],[5,1,2,3,4],[4,5,1,2,3],[3,4,5,1,2],[2,3,4,5,1]])

        self.longMessage = True

        for row in range(0,5):
            for tt in range(0,5):
                self.assertEqual(tt+1,mat.get_wall_for_row_and_type(row,tt),f'Row={row} Type={tt}')

    def test_move_tiles_to_row_fill_from_zero(self):
        mat = player_mat()
        mat.move_tiles_to_row(4,1,3)

        self.assertEqual(4, mat.get_floor_for_row_and_type(3,1))

    def test_move_tiles_to_row_partially_fill(self):
        mat = player_mat()
        mat.move_tiles_to_row(2,1,3)

        self.assertEqual(2, mat.get_floor_for_row_and_type(3,1))

    def test_move_tiles_to_row_fill(self):
        mat = player_mat()
        mat.move_tiles_to_row(2,1,3)
        mat.move_tiles_to_row(2,1,3)

        self.assertEqual(4, mat.get_floor_for_row_and_type(3,1))

    def test_move_tiles_to_row_overfill(self):
        mat = player_mat()
        mat.move_tiles_to_row(7,1,3)

        self.assertEqual(4, mat.get_floor_for_row_and_type(3,1))
        self.assertEqual(3, mat.get_nbr_tiles_in_penalty())

    def test_move_tiles_to_row_already_full_row(self):
        mat = player_mat()
        mat.move_tiles_to_row(4,1,3)

        with self.assertRaises(AssertionError):
            mat.move_tiles_to_row(4,1,3)

#   def test_has_a_completed_row(self):
#       self.fail('Not implemented')

#   def test_get_rows_permitted_for_tile_type(self):
#       self.fail('Not implemented')

    def test_process_end_of_round_basic(self):
        mat = player_mat()

        # fill row 0 with Azul
        mat.move_tiles_to_row(1,0,0)
        # fill row 4 with Black
        mat.move_tiles_to_row(5,3,4)
        # partially fill row 3 with Black
        mat.move_tiles_to_row(2,3,3)

        ended_game, discard = mat.process_end_of_round()

        # it is not the end of the game
        self.assertFalse(ended_game)

        # for a floor stack that was complete
        # the wall should be updated for the right tile type
        # the floor stack should be empty
        self.assertEqual(1,mat.get_wall_for_row_and_type(0,0))
        self.assertEqual(0, sum(mat.floor[0]))
        self.assertEqual(1,mat.get_wall_for_row_and_type(4,3))
        self.assertEqual(0, sum(mat.floor[4]))

        # for a floor stack that was incomplete
        # the wall should be not have changed
        # the floor stack should not be changed
        self.assertEqual(0,mat.get_wall_for_row_and_type(3,3))
        self.assertEqual(2, sum(mat.floor[3]))

        # penalty stack is now empty
        self.assertEqual(0,mat.get_nbr_tiles_in_penalty())

        # score changed properly
        self.assertEqual(2, mat.cummulative_score)

        # all the tiles removed from the floor stack should be returned so that they can go in the discard
        self.assertEqual(discard, [0,0,0,4,0,0])

    def test_process_end_of_round_basic_with_penalty(self):
        mat = player_mat()

        # fill row 0 with Azul
        mat.move_tiles_to_row(1,0,0)
        # fill row 4 with Black
        mat.move_tiles_to_row(7,3,4) # this should put 2 in penalty
        # partially fill row 3 with Black
        mat.move_tiles_to_row(2,3,3)

        mat.add_penalty_tile_to_penalty_stack()

        ended_game, discard = mat.process_end_of_round()

        # it is not the end of the game
        self.assertFalse(ended_game)

        # for a floor stack that was complete
        # the wall should be updated for the right tile type
        # the floor stack should be empty
        self.assertEqual(1,mat.get_wall_for_row_and_type(0,0))
        self.assertEqual(0, sum(mat.floor[0]))
        self.assertEqual(1,mat.get_wall_for_row_and_type(4,3))
        self.assertEqual(0, sum(mat.floor[4]))

        # for a floor stack that was incomplete
        # the wall should be not have changed
        # the floor stack should not be changed
        self.assertEqual(0,mat.get_wall_for_row_and_type(3,3))
        self.assertEqual(2, sum(mat.floor[3]))

        # penalty stack is now empty
        self.assertEqual(0,mat.get_nbr_tiles_in_penalty())

        # score changed properly
        self.assertEqual(0, mat.cummulative_score) # +2 -4

        # all the tiles removed from the floor stack should be returned so that they can go in the discard
        self.assertEqual(discard, [0,0,0,6,0,1])

 #  def test_add_tiles_to_penalty(self):
 #      self.fail('Not implemented')

#   def test_set_wall_for_row_and_type(self):
#       self.fail('Not implemented')

#   def test_add_penalty_tile_to_penalty_stack(self):
#       self.fail('Not implemented')

#   def test_get_nbr_tiles_in_penalty(self):
#       self.fail('Not implemented')

#   def test_get_total_tile_count(self):
#       self.fail('Not implemented')

#   def test_get_total_score(self):
#       self.fail('Not implemented')

    def test_get_score_for_wall_tile_empty_wall(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(1,0,1)
        self.assertEqual(1,mat.get_score_for_wall_tile(1,0))

    # 0 1 2 3 4
    # 4 0 1 2 3
    # 3 4 0 1 2
    # 2 3 4 0 1
    # 1 2 3 4 0 
    def test_get_score_for_wall_tile_1_row_streak(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(1,0,1)
        mat.set_wall_for_row_and_type(2,4,1)
        self.assertEqual(2,mat.get_score_for_wall_tile(1,0))

    def test_get_score_for_wall_tile_1_col_streak(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(1,0,1)
        mat.set_wall_for_row_and_type(1,1,1)
        self.assertEqual(2,mat.get_score_for_wall_tile(1,0))

    def test_get_score_for_wall_tile_col_and_row_streak(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(1,0,1)
        mat.set_wall_for_row_and_type(1,1,1)
        mat.set_wall_for_row_and_type(1,2,1)
        mat.set_wall_for_row_and_type(2,4,1)
        self.assertEqual(5,mat.get_score_for_wall_tile(1,0))

    def test_get_score_for_wall_tile_col_and_row_streak_extra_wall(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(2,0,1)
        mat.set_wall_for_row_and_type(1,1,1)
        mat.set_wall_for_row_and_type(0,2,1)
        mat.set_wall_for_row_and_type(2,3,1)
        mat.set_wall_for_row_and_type(2,4,1)
        mat.set_wall_for_row_and_type(2,2,1) #no connection
        mat.set_wall_for_row_and_type(4,3,1) #no connection
        mat.set_wall_for_row_and_type(4,4,1) #no connection
        self.assertEqual(6,mat.get_score_for_wall_tile(2,0))

    def test_get_score_for_wall_tile_back_corner(self):
        mat = player_mat()
        mat.set_wall_for_row_and_type(4,0,1)
        mat.set_wall_for_row_and_type(3,1,1)
        mat.set_wall_for_row_and_type(2,2,1)
        mat.set_wall_for_row_and_type(4,4,1)
        mat.set_wall_for_row_and_type(4,3,1)
        mat.set_wall_for_row_and_type(4,2,1)
        mat.set_wall_for_row_and_type(3,0,1) # no connection
        self.assertEqual(7,mat.get_score_for_wall_tile(4,0))

if __name__ == '__main__':
    unittest.main()
