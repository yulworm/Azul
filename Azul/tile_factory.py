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

        # replace tiles from discard to bag if needed
        if sum(self.bag) == 0:
            self.bag = self.discard.copy()
            self.discard = list()

        # add 4 tiles to each pile and remove them from the bag
        for i in range(1, self.nbr_piles):
            for tile in np.random.choice(self.bag, 4, replace=False):
                self.piles[i][tile] += 1
                self.bag.remove(tile)

        if self.dev_mode:
            #print(self)
            assert tile_cnt == self.get_total_tile_count(), f'Tile count changed from {tile_cnt} to {self.get_total_tile_count()}'

            self._is_coherent()


    def get_piles_with_tile_type(self, tile_type):
        """
        return a list of tuples containing (pile_idx, tile_type_count)
        """
        piles = list()

        for i in range(0, self.nbr_piles):
            if self.piles[i][tile_type] > 0:
                piles.append((i,self.piles[i][tile_type]))

        return piles

    def _is_coherent(self):
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

    def get_total_tile_count(self):
        total_tiles = 0
        for i in range(0, self.nbr_piles):
            #print(f'{i} current={total_tiles} + {sum(self.piles[i])}')
            total_tiles += sum(self.piles[i])

        #print(f'current={total_tiles} + {len(self.bag) + len(self.discard)}')
        total_tiles += len(self.bag) + len(self.discard)

        return total_tiles

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