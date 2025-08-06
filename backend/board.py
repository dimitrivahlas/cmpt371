from square import *

class Board:
    def __init__(self, rows=8, cols=8, square_size=80):
        self.rows = rows
        self.cols = cols
        self.square_size = square_size
        self.grid = [[Square(r, c, square_size) for c in range(cols)] for r in range(rows)]

    def draw(self, screen):
        for row in self.grid:
            for square in row:
                square.draw(screen)