import pygame
import sys
from modules.Board import Board
from modules.GamePiece import Snake


def runGame():
    pygame.init()
    pygame.key.set_repeat(50, 200)
    board = Board((400, 400), (10, 10))
    snake = Snake((4, 4), board)
    snake.head.draw()
    clock = pygame.time.Clock()
    while True:
        snake.head.move()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    runGame()
