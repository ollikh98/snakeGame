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
    grid_size = (5,5)
    snake_init_pos = (int(grid_size[0]/2),int(grid_size[0]/2))
    tile_size, _ = calc_tile_size(resolution, grid_size)
    coord_mapping = make_coord_mapping(resolution, tile_size)
    snake = Snake(coord_mapping, snake_init_pos, tile_size)
    apple = Apple(coord_mapping, tile_size, color='red')
    board = Board(coord_mapping, resolution, grid_size, tile_size, snake, apple)
    board.update()

    for i in range(0, 3, -1):
        f"{i}..."
        time.sleep(1)
    print('GO! ')

    return board


def game_loop(snake, apple):
    apple_collected = apple.collected(snake.head.game_pos, snake.occupied_tiles)
    if apple_collected:
        snake.extend()
    return snake.slither()


if __name__ == "__main__":
    clock = pygame.time.Clock()
    while True:
        game_board = game_init()
        while True:
            legal_move = game_loop(game_board.snake, game_board.apple)
            if not legal_move:
                print('COLLISION - RESTARTING')
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)
            game_board.update()