import pygame

white = (255, 255, 255)
grid_colour = (0, 0, 255)

class Square:
    def __init__(self, row, col, size):
        self.row = row
        self.col = col
        self.size = size
        self.color = white

    def draw(self, screen):
        rect = pygame.Rect(self.col * self.size, self.row * self.size, self.size, self.size)
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, grid_colour, rect, 1)