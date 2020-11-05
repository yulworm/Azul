import os
import pygame
import Azul_game

C_BACKGROUND = (255,255,255)
C_GRID_LINE = (195,195,195)#(128,128,128)
C_TILE_BACKGROUND = (195,195,195)
C_SCORE_TEXT = (100,100,100)
TILE_SIZE = (30,30)
GRID_LINE_WIDTH = 10
CELL_DIM = ((TILE_SIZE[0] + GRID_LINE_WIDTH),(TILE_SIZE[1] + GRID_LINE_WIDTH))
tile_images = list()
tile_backgrounds = [(192,220,232),(243,185,85),(244,150,155),(28,29,32),(255,255,255)]     #['A', 'Y', 'R', 'B', 'W', 'P']
from_tiles = list() # data = (rect, tile type, pile index)
to_row = list()
TILE_NAMES = ['Azul', 'Yellow', 'Red', 'Black', 'White', '1st player']
PILE_NAMES = ['Centre', '12', '3', '5', '7', '9']
ROW_NAMES = ['1', '2', '3', '4', '5', 'Penalty']
player_info = [['Player 1', None], ['Player 2', None]]

def play(ai):
    game = Azul_game.Azul_game()

    # game dimension = 36 x 12

    while game.winner is None:
        if game.current_player_idx == 1:
            action = ai.choose_action(game)
            game.move( action )
        else:
            #wait for player
            pass

def draw_game(game, surface):
    
    draw_player_mat(game, convert_cell_to_display_coords(0,0), surface, 0)

    draw_factory(game.factory, convert_cell_to_display_coords(13,0), surface)

    draw_player_mat(game, convert_cell_to_display_coords(25,0), surface, 1)

def draw_player_mat(game, coords, surface, player_idx):
    #sub_s = surface.subsurface((coords[0], coords[1], CELL_DIM[0]*13, CELL_DIM[1]*12))
    #sub_s.fill(C_GRID_LINE)
    mat = game.players[player_idx]

    # we reset the to_row so that it only contains the positions of the current player
    if game.current_player_idx == player_idx:
       to_row.clear()
       pass

    # draw wall grid
    contents = mat.get_wall_for_display()
    layout = mat.get_wall_layout()
    wall_start = convert_cell_to_display_coords(1,3)
    wall_start = (wall_start[0]+coords[0], wall_start[1]+coords[1])
    for i in range(5):
        for j in range(5):
            x = wall_start[0] + CELL_DIM[0]*j
            y = wall_start[1] + CELL_DIM[1]*i
            pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(surface, tile_backgrounds[layout[i][j]], (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i][j],(x,y),surface)
    
    # draw floor
    contents = mat.get_floor_for_display()
    floor_start = convert_cell_to_display_coords(7,3)
    floor_start = (floor_start[0]+coords[0], floor_start[1]+coords[1])
    #print(f'draw floor {contents}')
    for i in range(5):
        for j in range(len(contents[i])):
            #print(f'floor cell {i} {j} {contents[i][j]}')
            x = floor_start[0] + CELL_DIM[0]*j
            y = floor_start[1] + CELL_DIM[1]*i
            rect = pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i][j],(x,y),surface)
            if j == 0 and game.current_player_idx == player_idx:
                to_row.append((rect, i))

    # penalty
    penalty_start = convert_cell_to_display_coords(1,9)
    penalty_start = (penalty_start[0]+coords[0], penalty_start[1]+coords[1])
    contents = mat.get_penalty_stack_for_display()
    for i in range(2):
        for j in range(7):
            x = penalty_start[0] + CELL_DIM[0]*j
            y = penalty_start[1] + CELL_DIM[1]*i
            rect = pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            if len(contents) > i*7 + j:
                draw_tile(contents[i*7 + j],(x,y),surface)
            if i*7 + j == 0 and game.current_player_idx == player_idx:
                to_row.append((rect, 5))
            # yes, there could be extra tiles, but it doesn't affect the score after 7 anyway

    # Name 
    font = pygame.font.SysFont(None, 36)
    name_text = f'{player_info[player_idx][0]}'
    if game.current_player_idx == player_idx:
        name_text = f'{name_text} - Current player'
    name_img = font.render(name_text, True, (128,128,128))
    name_start = convert_cell_to_display_coords(2,1)
    name_start = (name_start[0]+coords[0], name_start[1]+coords[1])
    surface.blit(name_img, name_start)

    # score
    font = pygame.font.SysFont(None, 36)
    img = font.render(f'Score: {mat.get_total_score()}', True, (128,128,128))
    score_start = convert_cell_to_display_coords(2,2)
    score_start = (score_start[0]+coords[0], score_start[1]+coords[1])
    surface.blit(img, score_start)

    if game.winner == player_idx:
        flag = pygame.transform.scale(pygame.image.load(os.path.join('images','winner.jpg')),(120,160))
        flag.set_colorkey((254,254,254))
        flag_start = convert_cell_to_display_coords(9,0)
        flag_start = (flag_start[0]+coords[0], flag_start[1]+coords[1])
        surface.blit(flag, flag_start)

    # Last action or current player
    player_note = ''
    if game.current_player_idx != player_idx and player_info[player_idx][1] is not None:
        player_note = f'Last action: {get_action_for_display(player_info[player_idx][1])}'
    font = pygame.font.SysFont(None, 24)
    player_note_img = font.render(f'{player_note}', True, (128,128,128))
    player_note_start = convert_cell_to_display_coords(1,12)
    player_note_start = (player_note_start[0]+coords[0], player_note_start[1]+coords[1])
    surface.blit(player_note_img, player_note_start)

def draw_factory(factory, coords, surface):
    #sub_s = surface.subsurface((coords[0], coords[1], CELL_DIM[0]*11, CELL_DIM[1]*11))

    disp_piles = factory.get_piles_for_display()

    draw_centre_pile(disp_piles[0], convert_cell_to_display_coords(17,4), surface, 0)
     
    draw_outer_pile(disp_piles[1], convert_cell_to_display_coords(18,1), surface, 1)

    draw_outer_pile(disp_piles[2], convert_cell_to_display_coords(22,5), surface, 2)

    draw_outer_pile(disp_piles[3], convert_cell_to_display_coords(20,9), surface, 3)

    draw_outer_pile(disp_piles[4], convert_cell_to_display_coords(16,9), surface, 4)

    draw_outer_pile(disp_piles[5], convert_cell_to_display_coords(14,5), surface, 5)

def draw_centre_pile(contents, coords, surface, pile_idx):
    for i in range(4):
        for j in range(4):
            #print(f'floor cell {i} {j} {contents[i][j]}')
            x = coords[0] + CELL_DIM[0]*j
            y = coords[1] + CELL_DIM[1]*i
            rect = pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH, border_radius=0)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i*4 + j],(x,y),surface)
            if contents[i*4 + j] is not None:
                from_tiles.append((rect, contents[i*4 + j], pile_idx))

def draw_outer_pile(contents, coords, surface, pile_idx):
    for i in range(2):
        for j in range(2):
            x = coords[0] + CELL_DIM[0]*j
            y = coords[1] + CELL_DIM[1]*i
            rect = pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH, border_radius=0)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i*2 + j],(x,y),surface)
            if contents[i*2 + j] is not None:
                from_tiles.append((rect, contents[i*2 + j], pile_idx))

def load_tile_images():
    #['A', 'Y', 'R', 'B', 'W', 'P']
    
    #image = pygame.image.load(os.path.join('images','azul.png'))
    image = pygame.transform.scale(pygame.image.load(os.path.join('images','azul.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

    image = pygame.transform.scale(pygame.image.load(os.path.join('images','yellow.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

    image = pygame.transform.scale(pygame.image.load(os.path.join('images','red.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

    image = pygame.transform.scale(pygame.image.load(os.path.join('images','black.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

    image = pygame.transform.scale(pygame.image.load(os.path.join('images','white.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

    image = pygame.transform.scale(pygame.image.load(os.path.join('images','penalty.png')),(TILE_SIZE[0],TILE_SIZE[1]))
    image.set_colorkey((163,73,164))
    tile_images.append(image)

def draw_tile(ttype, coords, surface):
    if ttype is None:
        return
    #print(f'draw_tile {ttype}')
    surface.blit(tile_images[ttype],coords)

def convert_cell_to_display_coords(x, y):
    return ( CELL_DIM[0]*x, CELL_DIM[1]*y )

def get_action_for_display(action):
    return f'Move {action[3]} {TILE_NAMES[action[0]]} tiles from pile {PILE_NAMES[action[1]]} to row {ROW_NAMES[action[2]]}' 

def main():
     
    # initialize the pygame module
    pygame.init()

    # load and set the logo
    logo = pygame.image.load(os.path.join('images','logo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Azul")

    load_tile_images()
     
    # create a surface on screen 
    screen = pygame.display.set_mode((38*CELL_DIM[0],13*CELL_DIM[1]))
    bkg = pygame.transform.scale(pygame.image.load(os.path.join('images','background.jpg')),screen.get_size())
    screen.blit(bkg, (0,0))
    
    
    game = Azul_game.Azul_game()

    # define a variable to control the main loop
    running = True
     
    draw_game(game, screen)

    from_selected = (None,None,None) # rect, type, from
    to_selected = (None, None) # rect, to row
    selected_action = None
    action_text = ''
    # main loop
    while running:

        font = pygame.font.SysFont(None, 24)
        msg_img = font.render(action_text, True, (128,128,128))
        button_start = convert_cell_to_display_coords(14, 12)
        button_dim = (450, 35)
        button_colour = C_GRID_LINE
        if selected_action is not None:
            button_colour = (0,255,0)
        action_button = pygame.draw.rect(screen, button_colour, (button_start[0], button_start[1], button_dim[0], button_dim[1]))
        #font.size(action_text)[0], font.size(action_text)[1]
        #print(font.size(action_text))
        screen.blit(msg_img, (button_start[0] + (button_dim[0] - font.size(action_text)[0])//2, button_start[1] + (button_dim[1] - font.size(action_text)[1])//2))

        #draw_game(game, screen)
        pygame.display.flip()

        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = event.pos

                for from_rect, from_type, from_pile in from_tiles:
                    if from_rect.collidepoint(pos):
                        if from_selected[0] is None:
                            from_selected = (from_rect, from_type, from_pile)
                            pygame.draw.rect(screen, (0,255,0), (from_rect.x, from_rect.y, from_rect.width, from_rect.height), width=GRID_LINE_WIDTH)
                        else:
                            pygame.draw.rect(screen, C_GRID_LINE, (from_selected[0].x, from_selected[0].y, from_selected[0].width, from_selected[0].height), width=GRID_LINE_WIDTH)
                            from_selected = (from_rect, from_type, from_pile)
                            pygame.draw.rect(screen, (0,255,0), (from_rect.x, from_rect.y, from_rect.width, from_rect.height), width=GRID_LINE_WIDTH)
                        selected_action = None

                for to_rect, to_row_idx in to_row:
                    if to_rect.collidepoint(pos):
                        if to_selected[0] is None:
                            to_selected = (to_rect, to_row_idx)
                            pygame.draw.rect(screen, (0,255,0), (to_rect.x, to_rect.y, to_rect.width, to_rect.height), width=GRID_LINE_WIDTH)
                        else:
                            pygame.draw.rect(screen, C_GRID_LINE, (to_selected[0].x, to_selected[0].y, to_selected[0].width, to_selected[0].height), width=GRID_LINE_WIDTH)
                            to_selected = (to_rect, to_row_idx)
                            pygame.draw.rect(screen, (0,255,0), (to_rect.x, to_rect.y, to_rect.width, to_rect.height), width=GRID_LINE_WIDTH)
                        selected_action = None

                if action_button.collidepoint(pos) and selected_action is not None:
                    #print(f'taking action {selected_action}')
                    player_info[game.current_player_idx][1] = selected_action
                    game.move(selected_action)
                    screen.blit(bkg, (0,0))
                    from_selected = (None,None,None) # rect, type, from
                    to_selected = (None, None) # rect, to row
                    selected_action = None
                    draw_game(game, screen)

                # get the action that corresponds to the selected tile and row
                action_text = ''
                if from_selected[1] is not None and to_selected[1] is not None and selected_action is None:
                    for a_t_type, a_from_pile, a_to_row, a_nbr_tiles in game.available_actions(game):
                        if a_t_type == from_selected[1] and a_from_pile == from_selected[2] and a_to_row == to_selected[1]:
                            selected_action = (a_t_type, a_from_pile, a_to_row, a_nbr_tiles)
                            break

                    if selected_action is None:
                        action_text = 'Invalid selections'
                    else:
                        action_text = get_action_for_display(selected_action)



                
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()