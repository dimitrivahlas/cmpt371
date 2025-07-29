import pygame


#Initialize pygame
pygame.init()

#set up game swindow
tile_size = 100
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Deny and Conquer")


#Colour
black = (0,0,0) 

#fill game window with white
screen.fill((255,255,255))

#drawing grid
def draw_grid(tile_size):
    #fill game window with white
    screen.fill((255,255,255))

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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

#quit pygame
pygame.quit