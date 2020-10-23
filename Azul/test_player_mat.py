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

if __name__ == '__main__':
    unittest.main()
