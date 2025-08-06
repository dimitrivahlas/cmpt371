import sys
from board import *

rows = 8
cols = 8
square_size = 100
window_size = rows * square_size

def main():
    pygame.init()
    screen = pygame.display.set_mode((window_size, window_size))
    pygame.display.set_caption("8x8 Board Display")
    clock = pygame.time.Clock()

    board = Board(rows=rows, cols=cols, square_size=square_size)

    running = True
    while running:
        screen.fill((0, 0, 0))
        board.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()