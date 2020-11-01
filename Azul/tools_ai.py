import sys
import numpy as np

def get_complete_3D_action_list():
    """
    generates the list of all 3D actions
    """
    # Action is a tuple tile_type,nbr_to_move, row_to_move_to
    # 5 * 5 * 6 = 150 possibilities
    actions = list()
    for tt in range(0,5):
        for i in range(1,6): # the final value represents 5 or more
            for row in range(0,6):
                actions.append((tt,i,row))
    return actions

def convert_3D_action_to_game_action_random(a_3D,possible_game_actions):
    from_piles = set()
    for ga in get_filter_actions_containing_3D_action(a_3D, possible_game_actions):
        from_piles.add(ga[1])

    if len(from_piles) == 0:
        raise Exception(f'From could not be found for {a_3D} in {possible_game_actions}')

    return (a_3D[0], np.random.choice(list(from_piles)), a_3D[2], a_3D[1])

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

def get_3D_action_idxs_for_game_actions(game_actions,complete_action_list=None):
    if complete_action_list is None:
        complete_action_list = get_complete_3D_action_list()
    indexes = list()
    for a in convert_game_actions_to_3D_actions(game_actions):
        indexes.append( complete_action_list.index(a) )

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