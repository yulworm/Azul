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

    def test_has_a_completed_row(self):
        raise Exception()

if __name__ == '__main__':
    unittest.main()
