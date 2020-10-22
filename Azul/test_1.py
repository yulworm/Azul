import unittest
from tile_factory import tile_factory

class Test_test_1(unittest.TestCase):
    def test_factory_init(self):
        # there should be 100 tiles in the bag
        # the discard should be empty
        # all the piles should be empty except the centre which just has the pentalty tile
        self.fail("Not implemented")

    def test_fill_factory_piles(self):
        # the total number of tiles in the factory (excluding the discard) should be a multiple of 20 + 1
        # the centre pile should only have a pentalty tile
        self.fail("Not implemented")

if __name__ == '__main__':
    unittest.main()
