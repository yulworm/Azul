import unittest
import tools_ai
import Azul_game

class Test_test_tools_ai(unittest.TestCase):

    def test_convert_game_action_to_3D_action(self):
        self.assertEqual( tools_ai.convert_game_action_to_3D_action((0,1,3,2)), (0,2,3) )
        self.assertEqual( tools_ai.convert_game_action_to_3D_action((0,1,3,6)), (0,5,3) )
        self.assertEqual( tools_ai.convert_game_action_to_3D_action((4,2,4,1)), (4,1,4) )

    def test_get_3D_action_idxs_for_game_actions(self):
        # action type * 30 + nbr_to_move -1 * 6 + row_to
        self.assertEqual( tools_ai.get_3D_action_idxs_for_game_actions([(0,1,3,2)]), [9] ) # 0*30 + 1*6 + 3=9
        self.assertEqual( tools_ai.get_3D_action_idxs_for_game_actions([(0,1,3,2), (0,1,3,6)]), [9,27] ) # 0*30 + 4*6 + 3=27
        self.assertEqual( tools_ai.get_3D_action_idxs_for_game_actions([(0,1,3,2), (0,1,3,6), (4,2,4,1)]), [9,27,124] ) # 4*30 + 0*6 + 4=124

    def test_get_filter_actions_containing_3D_action(self):
        game_actions = [(0,1,3,2), (0,1,3,6), (4,2,4,1)]
        self.assertEqual( tools_ai.get_filter_actions_containing_3D_action((0,2,3), game_actions), [(0,1,3,2)] )

        game_actions.append((0,3,3,2))
        self.assertEqual( tools_ai.get_filter_actions_containing_3D_action((0,2,3), game_actions), [(0,1,3,2), (0,3,3,2)] )

if __name__ == '__main__':
    unittest.main()
