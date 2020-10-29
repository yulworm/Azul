import copy
class player_mat(object):
    """description of class"""

    tile_type_order = ['A', 'Y', 'R', 'B', 'W', 'P']
    nbr_stacks = 5
    def __init__(self):
        self.cummulative_score = 0

        self.penalty_stack = [0,0,0,0,0,0]

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
            if self.get_wall_for_row_and_type(row, tile_type) != 0:
                continue

            # there is room in the stack
            if self.floor[row][tile_type] < (row + 1):
                rows.append(row)
        return rows

    def get_floor_for_row_and_type(self, row, tile_type):
        """
        this method really only exists for testing
        """
        return self.floor[row][tile_type]

    def move_tiles_to_row(self, nbr_tiles, tile_type, row):
        # check that this is a permitted move for the type
        assert row in self.get_rows_permitted_for_tile_type(tile_type)

        space_in_stack = row + 1 - self.floor[row][tile_type]

        self.floor[row][tile_type] += min(space_in_stack, nbr_tiles)

        # put the overflow in the penalty
        self.add_tiles_to_penalty(max((nbr_tiles - space_in_stack), 0), tile_type)


    def process_end_of_round(self):
        """
        return tuple (
            True is the player ended the game, otherwise False
            List of tiles to be discarded
            )
        """
        discard = self.penalty_stack.copy()

        # loop through rows
        for row in range(0,5):
            # check for completed floor stacks
            if sum(self.floor[row]) == row + 1:
                # for the tile type that is in the stack
                for tt in range(0,5):
                    if self.floor[row][tt] > 0:
                        # mark wall tile
                        self.set_wall_for_row_and_type(row,tt,1)
            
                        # move all but one tile to discard
                        discard[tt] += self.floor[row][tt]-1

                        # set the floor to zero
                        self.floor[row][tt] = 0
            
                        # increase cummulative score
                        self.cummulative_score += self.get_score_for_wall_tile(row,tt)

        # decrease cummulative score by penalty - it can't go below 0
        self.cummulative_score = max(self.cummulative_score + self.get_penalty_score(), 0)

        # flush the penalty stack
        self.penalty_stack = [0,0,0,0,0,0]

        return (self.has_a_completed_row(), discard)

    def get_wall_for_row_and_type(self, row, tile_type):
        return self.wall[row][(tile_type+row)%5]

    def set_wall_for_row_and_type(self, row, tile_type, value):
        """
        sets the corresponding wall value
        Returns the wall index of the tile type
        """
        self.wall[row][(tile_type+row)%5] = value
        return (tile_type+row)%5

    def get_merged_wall_and_floor(self):
        """
        The method takes the information in the floor and merges it into the wall. A partially full floor stack becomes a fractional value in the wall
        Returns a wall list
        """
        ret_wall = copy.deepcopy( self.wall )
        # loop through rows
        for row in range(0,5):
            # check if anything is in the floor stack
            if sum(self.floor[row]) > 0:
                # for the tile type that is in the stack
                for tt in range(0,5):
                    if self.floor[row][tt] > 0:
                        # mark wall tile
                        ret_wall[row][(tt+row)%5] = self.floor[row][tt] / (row +1)

        return ret_wall

    def add_tiles_to_penalty(self, nbr_tiles, tile_type):
        self.penalty_stack[tile_type] += nbr_tiles

    def add_penalty_tile_to_penalty_stack(self):
        self.add_tiles_to_penalty(1, self.tile_type_order.index('P'))

    def set_wall_for_testing(self, values):
        """
        this is only to be used by unit tests
        the shape of the values is how it is stored, not tile type order
        """
        self.wall = values

    def get_nbr_tiles_in_penalty(self):
        return sum(self.penalty_stack)

    def get_total_tile_count(self):
        total_tiles = 0

        for i in range(0, self.nbr_stacks):
            total_tiles += sum(self.floor[i])

        for i in range(0, self.nbr_stacks):
            total_tiles += sum(self.wall[i])

        total_tiles += sum(self.penalty_stack)

        return total_tiles

    def get_penalty_score(self):
        # the penalty stack can contain more that 7 tiles, but we stop counting for penalties after 7
        pt = min(sum(self.penalty_stack), 7)

        # first 2 are -1 points each
        total = min(pt, 2) * -1
        
        # next 3 are -2 points each
        total += min(max(pt-2, 0), 3) * -2
        
        # next 2 are -3 points each
        total += min(max(pt-5, 0), 2) * -3
        
        return total

    def get_score_for_wall_tile(self,row,tile_type):
        col = (tile_type+row)%5

        col_score = 0
        row_score = 0

        col_streak_has_tile = False
        row_streak_has_tile = False
        col_streak = 0
        row_streak = 0

        for i in range(0,5):
            # row streak broken
            if self.wall[row][i] == 0:
                if row_streak_has_tile:
                    break
                else:
                    row_streak = 0
            else:
                row_streak += self.wall[row][i]
                # we are either already knew we were in a streak, or we just found out
                row_streak_has_tile = row_streak_has_tile or i==col

        if row_streak == 1:
            row_score = 0
        else:
            row_score = row_streak

        for i in range(0,5):
            # col streak broken
            if self.wall[i][col] == 0:
                if col_streak_has_tile:
                    break
                else:
                    col_streak = 0
            else:
                col_streak += self.wall[i][col]
                col_streak_has_tile = (col_streak_has_tile or (i==row))

        if col_streak == 1:
            col_score = 0
        else:
            col_score = col_streak

        return max(col_score + row_score, 1)

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
        for tt in range(1,5):
            if sum([self.get_wall_for_row_and_type(row, tt) for row in range(0,5)]) == 5:
                total_score += 10

        return total_score

    def has_a_completed_row(self):
        for i in range(0,5):
            if sum(self.wall[i]) + sum(self.floor[i])//(i+1) == 5:
                return True

        return False

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


        return return_str