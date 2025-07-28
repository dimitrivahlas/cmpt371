import pygame


#Initialize pygame
pygame.init()

#set up game swindow
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("hello pygame")

#game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

#quit pygame
pygame.quit