import unittest
from tile_factory import tile_factory
from player_mat import player_mat

class test_tile_factory(unittest.TestCase):
    nbr_piles = 6
    tile_type_order = player_mat.tile_type_order

    def test_factory_init(self):
        
        factory = tile_factory(self.nbr_piles,self.tile_type_order)

        # there should be 101 tiles total
        self.assertEqual( factory.get_total_tile_count(), 101 )

        # there should be 100 tiles in the bag
        self.assertEqual( factory.get_tile_count_in_bag(), 100 )

        # the discard should be empty
        self.assertEqual( factory.get_tile_count_in_discard(), 0 )

        # all the piles should be empty except the centre which just has the pentalty tile
        self.assertEqual( factory.get_tile_count_in_piles(), 1 )
        self.assertEqual( factory.get_tile_count_in_centre_pile(), 1 )

    def test_fill_factory_piles_basic(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)

        # we should be able to fill the piles completely 5 times
        for i in range(0,5):
            self.assertTrue( factory.fill_factory_piles() )

            # test that all the piles are full
            for pile_idx in range(1,factory.nbr_piles):
                self.assertEqual(sum(factory.piles[pile_idx]), 4, f'Pile {pile_idx} not full on iteration {i}, only has {sum(factory.piles[pile_idx])}')

            # centre pile should only have the penalty tile
            self.assertEqual(sum(factory.piles[0]),1, f'Centre pile has {sum(factory.piles[0])} tiles instead of 1 on iteration {i}')

            # empty the piles
            self.empty_all_piles(factory)

            factory.return_penalty_tile_to_centre()

    def test_fill_factory_piles_not_enough_in_bag_discard_empty(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_bag_contents([2,4,1,4,0,0]) #11 total
        self.assertTrue( factory.fill_factory_piles() )

        self.assertEqual(12, factory.get_tile_count_in_piles())
        self.assertEqual(1, factory.get_count_for_pile(0))
        self.assertEqual(4, factory.get_count_for_pile(1))
        self.assertEqual(4, factory.get_count_for_pile(2))
        self.assertEqual(3, factory.get_count_for_pile(3))
        self.assertEqual(0, factory.get_count_for_pile(4))
        self.assertEqual(0, factory.get_count_for_pile(5))

        self.assertEqual(0, factory.get_tile_count_in_bag())
        self.assertEqual(0, factory.get_tile_count_in_discard())
        
    def test_fill_factory_piles_not_enough_in_bag_discard_has_more_than_enough(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_bag_contents([2,4,1,4,0,0]) #11 total
        factory.add_tiles_to_discard([3,0,5,2,6,0]) #16 total
        self.assertTrue( factory.fill_factory_piles() )

        self.assertEqual(21, factory.get_tile_count_in_piles())
        self.assertEqual(1, factory.get_count_for_pile(0))
        self.assertEqual(4, factory.get_count_for_pile(1))
        self.assertEqual(4, factory.get_count_for_pile(2))
        self.assertEqual(4, factory.get_count_for_pile(3))
        self.assertEqual(4, factory.get_count_for_pile(4))
        self.assertEqual(4, factory.get_count_for_pile(5))

        self.assertEqual(7, factory.get_tile_count_in_bag())
        self.assertEqual(0, factory.get_tile_count_in_discard())

    def test_fill_factory_piles_not_enough_in_bag_discard_does_not_have_enough(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_bag_contents([2,4,1,4,0,0]) #11 total
        factory.add_tiles_to_discard([0,0,0,0,6,0]) #6 total
        self.assertTrue( factory.fill_factory_piles() )

        self.assertEqual(18, factory.get_tile_count_in_piles())
        self.assertEqual(1, factory.get_count_for_pile(0))
        self.assertEqual(4, factory.get_count_for_pile(1))
        self.assertEqual(4, factory.get_count_for_pile(2))
        self.assertEqual(4, factory.get_count_for_pile(3))
        self.assertEqual(4, factory.get_count_for_pile(4))
        self.assertEqual(1, factory.get_count_for_pile(5))

        self.assertEqual(0, factory.get_tile_count_in_bag())
        self.assertEqual(0, factory.get_tile_count_in_discard())


    def test_fill_factory_piles_bag_and_discard_empty(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_bag_contents([0,0,0,0,0,0])
        self.assertFalse( factory.fill_factory_piles() )

    def test_remove_tiles_from_pile_to_empty_centre(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        
        factory.set_pile_contents(1,[1,2,1,0,0,0])

        remove_ret = factory.remove_tiles_from_pile(1,0)

        # did it return the right counts?
        self.assertEqual(remove_ret, (1,0))

        # the pile should now be empty
        self.assertEqual(factory.get_count_for_pile(1), 0)

        # the centre should now have all the tiles except for the one removed
        self.assertEqual(factory.get_tile_count_in_centre_pile(), 4 )

    def test_remove_tiles_from_pile_to_not_empty_centre(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        
        factory.set_pile_contents(1,[1,2,1,0,0,0])
        factory.set_pile_contents(0,[1,0,1,2,0,1])

        remove_ret = factory.remove_tiles_from_pile(1,0)

        # did it return the right counts?
        self.assertEqual(remove_ret, (1,0))

        # the pile should now be empty
        self.assertEqual(factory.get_count_for_pile(1), 0)

        # the centre should now have all the tiles except for the one removed, plus those there in the beginning
        self.assertEqual(factory.get_tile_count_in_centre_pile(), 8 )

        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,0), 1)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,1), 2)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,2), 2)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,3), 2)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,4), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,5), 1)

    def test_remove_tiles_from_centre(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        
        factory.set_pile_contents(0,[1,0,1,2,0,1])

        remove_ret = factory.remove_tiles_from_pile(0,3)

        # did it return the right counts?
        self.assertEqual(remove_ret, (2,1))

        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,0), 1)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,1), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,2), 1)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,3), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,4), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,5), 0)

    def test_remove_tiles_from_centre_no_penalty(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        
        factory.set_pile_contents(0,[1,0,1,2,0,0])

        remove_ret = factory.remove_tiles_from_pile(0,3)

        # did it return the right counts?
        self.assertEqual(remove_ret, (2,0))

        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,0), 1)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,1), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,2), 1)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,3), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,4), 0)
        self.assertEqual(factory.get_count_for_pile_and_tile_type(0,5), 0)

    def test_set_bag_contents(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_bag_contents([2,4,0,1,6,0])
        self.assertEqual(factory.bag, [0,0,1,1,1,1,3,4,4,4,4,4,4])

    def test_set_pile_contents(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.add_tiles_to_discard([2,4,0,1,6,0])
        self.assertEqual(factory.discard, [0,0,1,1,1,1,3,4,4,4,4,4,4])

    def test_get_piles_with_tile_type(self):
        # find single, count 1
        # find single, count 3
        # find none
        # find multiple
        # ring pile
        # centre pile
        raise Exception()

    def test_return_penalty_tile(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        factory.set_pile_contents(0,[0,0,0,0,0,0])

        self.assertEqual(0, factory.get_tile_count_in_piles())

        factory.return_penalty_tile_to_centre()
        
        self.assertEqual(1, factory.get_tile_count_in_piles())
        self.assertEqual(1, factory.get_tile_count_in_centre_pile())

    def test_get_total_tile_count(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        self.assertEqual(101, factory.get_total_tile_count())

        factory.fill_factory_piles()
        self.assertEqual(101, factory.get_total_tile_count())

        factory.set_bag_contents([2,4,0,1,6,0]) #13
        self.assertEqual(34, factory.get_total_tile_count()) #101-80+13

    def test_get_total_tile_count_2(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        
        factory.set_bag_contents([0,0,0,0,0,0]) 
        self.assertEqual(1, factory.get_total_tile_count())

        factory.set_pile_contents(1,[1,0,1,2,0,0])
        self.assertEqual(5, factory.get_total_tile_count())

        remove_ret = factory.remove_tiles_from_pile(1,3)
        self.assertEqual(3, factory.get_total_tile_count())
    
    def test_get_count_for_pile_and_tile_type(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_get_count_for_pile(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_get_tile_count_in_centre_pile(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_get_tile_count_in_piles(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_get_tile_count_in_bag(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_get_tile_count_in_discard(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()

    
    def test_add_tiles_to_discard(self):
        factory = tile_factory(self.nbr_piles,self.tile_type_order)
        raise Exception()



    def empty_all_piles(self, factory):
        for i in range(1,factory.nbr_piles):
            # loop through the tile types until something was removed from the pile. When that happens, we go on to the next pile
            for j in range(0,5):
                if factory.remove_tiles_from_pile(i,j)[0] > 0:
                    break

        # loop through the tile types removing from the centre pile
        for j in range(0,5):
            factory.remove_tiles_from_pile(0,j)

if __name__ == '__main__':
    unittest.main()
