import sys

def get_3D_action_list():
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
    tile_type, from_row, to_row, nbr_to_move = ga

    return (tile_type, min(nbr_to_move,5), to_row)

def convert_game_actions_to_3D_actions(game_actions):
    actions = list()
    for ga in game_actions:
        actions.append( convert_game_action_to_3D_action(ga) )
    return actions

def get_3D_action_idxs_for_game_actions(game_actions):
    nas = get_3D_action_list()
    indexes = list()
    for a in convert_game_actions_to_3D_actions(game_actions):
        indexes.append( nas.index(a) )

    return indexes

def get_filter_actions_containing_3D_action(action_3D, game_actions):
    filtered_list = list()
    for ga in game_actions:
        if convert_game_action_to_3D_action(ga) == action_3D:
            filtered_list.append(ga)
    return filtered_list

def progress(count, total, status=''):
    """
    From https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    """
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()