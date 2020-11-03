import os
import pygame
import Azul_game

C_BACKGROUND = (255,255,255)
C_GRID_LINE = (128,128,128)
C_TILE_BACKGROUND = (195,195,195)
TILE_SIZE = (30,30)
GRID_LINE_WIDTH = 5
CELL_DIM = ((TILE_SIZE[0] + GRID_LINE_WIDTH),(TILE_SIZE[1] + GRID_LINE_WIDTH))
tile_images = list()
tile_backgrounds = [(192,220,232),(243,185,85),(244,150,155),(28,29,32),(255,255,255)]     #['A', 'Y', 'R', 'B', 'W', 'P']

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

    draw_player_mat(game.players[0], convert_cell_to_display_coords(0,0), surface)

    draw_factory(game.factory, convert_cell_to_display_coords(13,0), surface)

    draw_player_mat(game.players[1], convert_cell_to_display_coords(25,0), surface)

def draw_player_mat(mat, coords, surface):
    sub_s = surface.subsurface((coords[0], coords[1], CELL_DIM[0]*13, CELL_DIM[1]*12))
    #sub_s.fill(C_GRID_LINE)

    # draw wall grid
    contents = mat.get_wall_for_display()
    layout = mat.get_wall_layout()
    wall_start = convert_cell_to_display_coords(1,3)
    for i in range(5):
        for j in range(5):
            x = wall_start[0] + CELL_DIM[0]*j
            y = wall_start[1] + CELL_DIM[1]*i
            pygame.draw.rect(sub_s, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(sub_s, tile_backgrounds[layout[i][j]], (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i][j],(x,y),sub_s)
    
    # draw floor
    contents = mat.get_floor_for_display()
    floor_start = convert_cell_to_display_coords(7,3)
    #print(f'draw floor {contents}')
    for i in range(5):
        for j in range(len(contents[i])):
            #print(f'floor cell {i} {j} {contents[i][j]}')
            x = floor_start[0] + CELL_DIM[0]*j
            y = floor_start[1] + CELL_DIM[1]*i
            pygame.draw.rect(sub_s, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(sub_s, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i][j],(x,y),sub_s)

    # penalty
    penalty_start = convert_cell_to_display_coords(1,9)
    contents = mat.get_penalty_stack_for_display()
    for i in range(2):
        for j in range(7):
            x = penalty_start[0] + CELL_DIM[0]*j
            y = penalty_start[1] + CELL_DIM[1]*i
            pygame.draw.rect(sub_s, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH)
            pygame.draw.rect(sub_s, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            if len(contents) > i*2 + j:
                draw_tile(contents[i*2 + j],(x,y),sub_s)
            # yes, there could be extra tiles, but it doesn't affect the score after 7 anyway

def draw_factory(factory, coords, surface):
    sub_s = surface.subsurface((coords[0], coords[1], CELL_DIM[0]*11, CELL_DIM[1]*11))

    disp_piles = factory.get_piles_for_display()

    draw_centre_pile(disp_piles[0], convert_cell_to_display_coords(4,4), sub_s)
     
    draw_outer_pile(disp_piles[1], convert_cell_to_display_coords(5,1), sub_s)

    draw_outer_pile(disp_piles[2], convert_cell_to_display_coords(9,5), sub_s)

    draw_outer_pile(disp_piles[3], convert_cell_to_display_coords(7,9), sub_s)

    draw_outer_pile(disp_piles[4], convert_cell_to_display_coords(3,9), sub_s)

    draw_outer_pile(disp_piles[5], convert_cell_to_display_coords(1,5), sub_s)

def draw_centre_pile(contents, coords, surface):
    for i in range(4):
        for j in range(4):
            #print(f'floor cell {i} {j} {contents[i][j]}')
            x = coords[0] + CELL_DIM[0]*j
            y = coords[1] + CELL_DIM[1]*i
            pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH, border_radius=0)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i*4 + j],(x,y),surface)

def draw_outer_pile(contents, coords, surface):
    for i in range(2):
        for j in range(2):
            x = coords[0] + CELL_DIM[0]*j
            y = coords[1] + CELL_DIM[1]*i
            pygame.draw.rect(surface, C_GRID_LINE, (x, y, TILE_SIZE[0], TILE_SIZE[1]), width=GRID_LINE_WIDTH, border_radius=0)
            pygame.draw.rect(surface, C_TILE_BACKGROUND, (x, y, TILE_SIZE[0], TILE_SIZE[1]))
            draw_tile(contents[i*2 + j],(x,y),surface)

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

def main():
     
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
    logo = pygame.image.load(os.path.join('images','logo.png'))
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Azul")

    load_tile_images()
     
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((38*CELL_DIM[0],13*CELL_DIM[1]))
    bkg = pygame.transform.scale(pygame.image.load(os.path.join('images','background.jpg')),screen.get_size())
    screen.blit(bkg, (0,0))
    
    
    game = Azul_game.Azul_game()
    #game.players[0].move_tiles_to_row(3,4,4)

    # define a variable to control the main loop
    running = True
     
    draw_game(game, screen)

    # main loop
    while running:

        #draw_game(game, screen)
        pygame.display.flip()
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()