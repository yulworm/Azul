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

if __name__ == '__main__':
    unittest.main()
