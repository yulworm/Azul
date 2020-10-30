

def get_3d_action_list():
    # Action is a tuple tile_type,nbr_to_move, row_to_move_to
    # 5 * 5 * 6 = 150 possibilities
    actions = list()
    for tt in range(0,5):
        for i in range(1,6): # the final value represents 5 or more
            for row in range(0,6):
                actions.append((tt,i,row))
    return actions

def convert_game_action_to_3D_action(ga):
    """
    game action
        - tile type we will be moving
        - from which pile will we draw the tiles
        - to which row will we be moving the tiles
        - the number of tiles to be moved
    3D action
        - tile type
        - number to move, max 5
        - row to move to
    """
    tile_type, from_row, nbr_to_move, to_row = ga

    return (tile_type, max(nbr_to_move,5), to_row)

def get_3D_action_idxs_for_game_actions(game_actions):
    nas = get_3D_action_list()
    indexes = list()
    for ga in game_actions:
        indexes.append( nas.index( convert_game_action_to_3D_action(ga) ) )

    return indexes