import pygame
import sys
import time
from modules.Board import Board
from modules.GamePiece import Snake


def gamestart():
    pygame.init()
    pygame.key.set_repeat(50, 200)
    board = Board((400, 400), (10, 10))
    snake = Snake((4, 4), board)
    snake.head.draw()
    print('3..')
    time.sleep(1)
    print('2..')
    time.sleep(1)
    print('1..')
    time.sleep(1)
    print('GO! ')

    return snake
def runGame(snake):
    collisionDetection = snake.head.move()

    return collisionDetection


if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:
        snake = gamestart()
        while True:
            collision = runGame(snake)
            if collision == -1:
                print('COLLISION - RESTARTING')
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)
