import pygame
import sys
import time
from modules.Board import Board
from modules.GamePiece import Snake, Apple
from modules.Utils import calctileSize, makeMap


def gamestart():
    pygame.init()
    pygame.key.set_repeat(50, 200)
    resolution = (400,400)
    grid_size = (10,10)
    tile_size, _ = calctileSize(resolution,grid_size)
    coord_mapping = makeMap(resolution,tile_size)
    print(coord_mapping)
    snake = Snake(coord_mapping,(4,4),tile_size)
    apple = Apple(coord_mapping,tile_size,color='red')
    board = Board(coord_mapping, resolution,grid_size,tile_size,snake,apple)
    # print('3..')
    # time.sleep(1)
    # print('2..')
    # time.sleep(1)
    # print('1..')
    time.sleep(1)
    print('GO! ')

    return board
def runGame(snake, apple):
    appleCollected = apple.collected(snake.head.game_pos)
    if appleCollected:
        snake.extend()
    snake.move()
    return snake.collision()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:
        board = gamestart()
        while True:
            collision = runGame(board.snake, board.apple)
            if collision:
                print('COLLISION - RESTARTING')
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)
            board.update()
