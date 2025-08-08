import pygame
from pygame.locals import *
import numpy as np
#from backend .client import send_tile_update we need this defined


#get the player id from clinet which needs to be implemented there
def set_player_id(player_id):
    global current_player
    current_player = player_id

#handling game over
def game_over(winner_id):
    print(f"player {winner_id} wins")
    pygame.quit

#Initialize pygame
pygame.init()

#Define diff player colours
player_colours = {
    1: (255,0,0), #red
    2: (0,255,0),#Green
    3: (0,0,255), # Blue
    4: (255,255,0), # yellow
}

current_player = 1 #for now hardcode until client is set up
#set up game swindow
tile_size = 100
screen_width = 800
grid_height = 800
leaderboard_height = 100
screen_height = grid_height + leaderboard_height

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Deny and Conquer")

#Colour
black = (0,0,0)

#fill game window with white
screen.fill((255,255,255))

# scribble surface
scribble_surf = pygame.Surface((screen_width, screen_height), SRCALPHA)
drawing = False
locked_tiles = {} #row,col
current_tile = None


pygame.font.init()
font = pygame.font.SysFont(None, 36)

total_tiles = (screen_width // tile_size) * (screen_height // tile_size)

def draw_leaderboard():
    pygame.draw.rect(screen, (255, 255, 255), (0, grid_height, screen_width, leaderboard_height))  # background
    pygame.draw.line(screen, (0, 0, 0), (0, grid_height), (screen_width, grid_height), 2)  # top border

    #Count score for each player
    scores = {pid: 0 for pid in player_colours}
    for owner in locked_tiles.values():
        scores[owner] += 1

    #Display scores
    x_offset = 10
    for pid, score in scores.items():
        color = player_colours[pid]
        text = font.render(f"P{pid}: {score}", True, color)
        screen.blit(text, (x_offset, grid_height + 30))
        x_offset += 200


#drawing grid
def draw_grid(tile_size):
    #fill game window with white
    screen.fill((255,255,255))
    screen.blit(scribble_surf, (0,0))

    #draw verticle lines
    for x in range(tile_size, screen_width,tile_size):
        pygame.draw.line(screen,black, (x,0), (x,screen_height))

    #draw horizontal lines
    for y in range(tile_size, screen_height, tile_size):
        pygame.draw.line(screen, black, (0,y), (screen_width,y))

#game loop
running = True
while running:

    #draw grid
    draw_grid(tile_size)
    draw_leaderboard()

    #event handler, add avents like on click, clikc hold, drawing lines
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            if event.rel[0] > 0:
                print("mosuing moving to the right")
            elif event.rel[1] > 0:
                print("Mouse moving down")
            elif event.rel[1] < 0:
                print("mouse moving up")
            elif event.rel[0] < 0:
                print("mouse moving left")
            if drawing and current_tile and current_tile not in locked_tiles:
                mx, my = event.pos
                col = mx // tile_size
                row = my // tile_size
                if (row, col) == current_tile:  # restrict to same tile
                    pygame.draw.circle(
                        scribble_surf,
                        player_colours[current_player],  # swap through diff players
                        event.pos,
                        2  # brush radius
                    )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Right mouse button pressed")
            mx, my = event.pos
            col = mx // tile_size
            row = my // tile_size
            tile = (row, col)
            if not drawing and tile not in locked_tiles:
                current_tile = tile
                drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            print("Mouse button has been released")
            if drawing and current_tile and current_tile not in locked_tiles:
                drawing = False
                row, col = current_tile
                x = col * tile_size
                y = row * tile_size
                tile_rect = pygame.Rect(x, y, tile_size, tile_size)
                tile_surface = scribble_surf.subsurface(tile_rect).copy()
                alpha = pygame.surfarray.array_alpha(tile_surface)
                filled_pixels = np.count_nonzero(alpha)
                total_pixels = tile_size * tile_size
                percent_filled = filled_pixels / total_pixels
                if percent_filled >= 0.5:
                    pygame.draw.rect(scribble_surf, player_colours[current_player], tile_rect)
                    locked_tiles[(row,col)] = current_player
                    #send_tile_update(row,col,current_player) not defined yet
                else:
                    pygame.draw.rect(scribble_surf, (255, 255, 255), tile_rect)
            drawing = False
            current_tile = None

    pygame.display.update()

#quit pygame
pygame.quit()

#will need to be ceint.py for updates
def update_tile_from_server(row, col, player_id):
    locked_tiles[(row, col)] = player_id
    x = col * tile_size
    y = row * tile_size
    tile_rect = pygame.Rect(x, y, tile_size, tile_size)
    pygame.draw.rect(scribble_surf, player_colours[player_id], tile_rect)