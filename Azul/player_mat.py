class player_mat(object):
    """description of class"""

    tile_type_order = ['A', 'Y', 'R', 'B', 'W', 'P']
    nbr_stacks = 5
    def __init__(self):
        #self.tile_type_order = tile_order

        self.cummulative_score = 0

        self.penalty_stack = [0,0,0,0,0,0,0]
        self.penalty_overflow = [0,0,0,0,0,0,0]

        self.floor = list()
        for i in range(0,self.nbr_stacks):
            self.floor.append([0,0,0,0,0])

        self.wall = list()
        for i in range(0,self.nbr_stacks):
            self.wall.append([0,0,0,0,0])

    def get_rows_permitted_for_tile_type(self, tile_type):
        rows = list()

        # a tile type is permitted in a row unless
        for row in range(0,5):
            # the floor already contains another tile type
            if sum(self.floor[row]) != self.floor[row][tile_type]:
                continue

            # the wall already contains that tile type
            if self.wall[row][(tile_type - row)%5] == 1:
                continue

            rows.append(row)
        return rows

    def get_total_tile_count(self):
        total_tiles = 0

        for i in range(0, nbr_stacks):
            total_tiles += sum(self.floor[i])

        for i in range(0, nbr_stacks):
            total_tiles += sum(self.wall[i])

        total_tiles += sum(self.penalty_stack)

        total_tiles += sum(self.penalty_overflow)

        return total_tiles

    def get_penalty_score(self):
        pt = sum(self.penalty_stack)
        assert 0 <= pt <= 7, f'Penalty stack has too high a total {pt} - {self.penalty_stack}'

        # first 2 are -1 points each
        total = min(pt, 2) * -1
        
        # next 3 are -2 points each
        total += min(max(pt-2, 0), 3) * -2
        
        # next 2 are -3 points each
        total += min(max(pt-5, 0), 2) * -3
        
        return total

    def get_total_score(self):
        total_score = self.cummulative_score

        # complete columns
        for i in range(0, self.nbr_stacks):
            if sum([row[i] for row in self.wall]) == 5:
                total_score += 7

        # complete rows
        for i in range(0, self.nbr_stacks):
            if sum(self.wall[i]) == 5:
                total_score += 2

        # complete tile types
        total_score += 0 # TODO:
        
        return total_score

    def __str__(self):
        return_str = f'Score={self.get_total_score()}\n'

        for i in range(0,self.nbr_stacks):
            nbr_blanks = 5 - i - 1

            nbr_filled = sum(self.floor[i])

            tile_type = -1
            tile_type_alpha = None
            if nbr_filled > 0:
                for k in range(0,5):
                    if self.floor[i][k] == nbr_filled:
                        tile_type = k
            
            tile_type_alpha = self.tile_type_order[tile_type]

            nbr_empty = 5 - nbr_blanks - nbr_filled

            for j in range(0,nbr_blanks):
                return_str += ' '

            for j in range(0,nbr_empty):
                return_str += '_'

            for j in range(0,nbr_filled):
                return_str += tile_type_alpha

            return_str += "\t"

            for k in range(0,5):
                return_str += f'{self.tile_type_order[(k-i)%5]}{self.wall[i][k]} '

            return_str += '\n'

        return_str += f'Penalty={self.get_penalty_score()}\t'

        for i in range(0, len(self.tile_type_order)):
            for j in range(0,self.penalty_stack[i]):
                return_str += self.tile_type_order[k]
        return_str += f'\n'


        return_str += f'Penalty Overflow\t'

        for i in range(0, len(self.tile_type_order)):
            for j in range(0,self.penalty_overflow[i]):
                return_str += self.tile_type_order[k]
        return_str += f'\n'

        return return_str