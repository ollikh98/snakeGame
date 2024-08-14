import pygame
import sys
import time
from modules.Board import Board
from modules.GamePiece import Snake, Apple
from modules.Utils import calc_tile_size, make_coord_mapping


def game_init():
    pygame.init()
    pygame.key.set_repeat(50, 200)
    resolution = (400, 400)
    grid_size = (10, 10)
    tile_size, _ = calc_tile_size(resolution, grid_size)
    coord_mapping = make_coord_mapping(resolution, tile_size)
    print(coord_mapping)
    snake = Snake(coord_mapping, (4, 4), tile_size)
    apple = Apple(coord_mapping, tile_size, color='red')
    board = Board(coord_mapping, resolution, grid_size, tile_size, snake, apple)

    for i in range(0, 3, -1):
        f"{i}..."
        time.sleep(1)
    print('GO! ')

    return board


def game_loop(snake, apple):
    apple_collected = apple.collected(snake.head.game_pos)
    if apple_collected:
        snake.extend()
    snake.move()
    return snake.collision()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:
        game_board = game_init()
        while True:
            collision = game_loop(game_board.snake, game_board.apple)
            if collision:
                print('COLLISION - RESTARTING')
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)
            game_board.update()