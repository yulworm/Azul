import numpy as np

class tile_factory(object):
    """description of class"""

    dev_mode = True

    def __init__(self, nbr_piles, tile_order):
        #self.piles = [[0,0,0,0,0,1]]

        self.nbr_piles = nbr_piles
        self.tile_type_order = tile_order

        self.piles = list()
        for i in range(0,self.nbr_piles):
            self.piles.append([0,0,0,0,0,0])

        self.piles[0][self.tile_type_order.index('P')] = 1

        self.bag = list()
        for i in range(0,5):
            for j in range(0,20):
                self.bag.append(i)
        
        self.discard = list()
        

    def fill_factory_piles(self):
        """
        return True if at least one tile was placed, otherwise False
        """
        tile_cnt = 0
        if self.dev_mode:
            # we assume that the penalty tile was placed in the centre by the previous step
            assert self.piles[0][self.tile_type_order.index('P')] == 1, f"Penalty tile is missing"

            # this method should never be called if the piles aren't empty (except for the penalty time)
            p_tiles = 0
            for i in range(0, self.nbr_piles):
                p_tiles += sum(self.piles[i])

            assert p_tiles == 1, 'The piles are not empty before calling fill_factory_piles'
            tile_cnt = self.get_total_tile_count()

        chosen_tiles = list()
        while len(chosen_tiles) < 20:
            # replace tiles from discard to bag if needed
            if len(self.bag) == 0:

                # if the discard is empty too, then we can't get more tiles
                if len(self.discard) == 0:
                    break
                else:
                    self.bag = self.discard.copy()
                    self.discard = list()

            nbr_tiles_missing = 20 - len(chosen_tiles)

            for tile in np.random.choice(self.bag, min(nbr_tiles_missing, len(self.bag)), replace=False):
                self.bag.remove(tile)
                chosen_tiles.append(tile)


        # add 4 tiles to each pile 
        for i in range(0,len(chosen_tiles)):
            self.piles[(i // 4) + 1][chosen_tiles[i]] += 1

        if self.dev_mode:
            #print(self)
            assert tile_cnt == self.get_total_tile_count(), f'Tile count changed from {tile_cnt} to {self.get_total_tile_count()}'

            self._is_coherent()

        return len(chosen_tiles) > 0

    def get_piles_with_tile_type(self, tile_type):
        """
        return a list of tuples containing (pile_idx, tile_type_count)
        """
        piles = list()

        for i in range(0, self.nbr_piles):
            if self.piles[i][tile_type] > 0:
                piles.append((i,self.piles[i][tile_type]))

        return piles

    def remove_tiles_from_pile(self,pile_idx,tile_type):
        """
        returns a tuple (nbr_tile_type_requested, penalty_tile)
        If the requested tile type is not in the pile, then (0,0) is returned
        If the type exists, then all other types in the pile are moved to the centre pile
        """
        return_vals = (0,0)
        if self.piles[pile_idx][tile_type] == 0:
            return return_vals

        return_vals = (self.piles[pile_idx][tile_type], self.piles[pile_idx][self.tile_type_order.index('P')])

        # remove the requested tile type and the penalty tile (if one was found). This can be done to any pile, even the centre
        self.piles[pile_idx][tile_type] -= return_vals[0]
        self.piles[pile_idx][self.tile_type_order.index('P')] -= return_vals[1]

        # if not drawing from the centre pile, then move the remaining tiles to the centre
        if pile_idx != 0:
            for i in range(0,5):
                self.piles[0][i] += self.piles[pile_idx][i]
                self.piles[pile_idx][i] = 0

        return return_vals

    def return_penalty_tile(self):
        # this should only be called if the stacks are empty
        assert self.get_tile_count_in_piles() == 0

        self.piles[0][self.tile_type_order.index('P')] = 1


    def get_total_tile_count(self):
        return self.get_tile_count_in_piles() + self.get_tile_count_in_bag() + self.get_tile_count_in_discard()

    def get_count_for_pile_and_tile_type(self, pile_idx, tile_type):
        return self.piles[pile_idx][tile_type]

    def get_count_for_pile(self, pile_idx):
        return sum(self.piles[pile_idx])

    def get_tile_count_in_centre_pile(self):
        return sum(self.piles[0])

    def get_tile_count_in_piles(self):
        total_tiles = 0
        for i in range(0, self.nbr_piles):
            total_tiles += sum(self.piles[i])

        return total_tiles

    def get_tile_count_in_bag(self):
        return len(self.bag)

    def get_tile_count_in_discard(self):
        return len(self.discard)

    def set_pile_contents(self, pile_idx, type_counts):
        """this method is only supposed to be used for testing"""
        assert len(type_counts) == len(self.tile_type_order)
        self.piles[pile_idx] = type_counts

    def set_bag_contents(self, type_counts):
        """this method is only supposed to be used for testing"""
        assert len(type_counts) == len(self.tile_type_order) -1
        self.bag = list()
        for tile_type in range(0, len(self.tile_type_order) -1):
            for i in range(0,type_counts[tile_type]):
                self.bag.append(tile_type)

    def add_tiles_to_discard(self, type_counts):
        # there should not be a penalty type
        assert len(type_counts) == len(self.tile_type_order) -1

        for type in range(0, len(self.tile_type_order) -1):
            for i in range(0, type_counts[type]):
                self.discard.append(type) 


    def __str__(self):

        out_str = 'Piles -------------\n'
        out_str += ' '
        for i in range(0,6):
            out_str += f'\t{self.tile_type_order[i]}'
        out_str += '\n'
        for i in range(0,self.nbr_piles):
            out_str += f'{i}'
            for j in range(0,6):
                out_str += f'\t{self.piles[i][j]}'
            out_str += '\n'

        out_str += f'Bag {self.bag}\n'

        out_str += f'Discard {self.discard}\n'

        return out_str

    def _is_coherent(self):
        """
        this method is used to test if the current state of the factory breaks any rules
        """

        # the number of piles is correct
        if len(self.piles) != self.nbr_piles:
            raise ValueError(f'There should be {self.nbr_piles} piles, but instead there are {len(self.piles)}')

        for i in range(0, self.nbr_piles):
            # the penalty tile is only ever in the centre pile
            if i > 0 and self.piles[i][self.tile_type_order.index('P')] != 0:
                raise ValueError(f'There is a penalty tile in pile {i}')
            
            # other than the centre pile, no pile has more than 4 tiles
            if i > 0 and sum(self.piles[i]) > 4:
                raise ValueError(f'Pile {i} has {sum(self.piles[i])}, but it should never have more than 4')

            for j in range(0, 6):
                # no tile should have a negative value
                if self.piles[i][j] < 0:
                    raise ValueError(f'Pile {i} Tile {j} has count = {self.piles[i][j]} but it should never be less than 0')

        # the sum of all tiles is not more than 101
        if self.get_total_tile_count() > 101:
            raise ValueError(f'There are {self.get_total_tile_count()}, but there should never be more than 101')

        return True