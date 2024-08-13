import pygame
from modules.GamePiece import Snake, Apple

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

# Board keeps track of active pieces, and drawing/frame updates
class Board:
    # TODO:
    #  setup 1/3 of the screen to be dedicated scoreboard: score, snake length, direction, key press etc.
    #  Maybe try interactive sliders on the side to adjust while screen still active?
    def __init__(self, coord_mapping, resolution, grid_size, tile_size, snake: Snake, apple: Apple):
        self.resolution = resolution
        self.width = grid_size[0]
        self.height = grid_size[1]
        self.snake = snake
        self.apple = apple
        self.tile_size = tile_size
        self.coord_mapping = coord_mapping
        self.board = pygame.display.set_mode(self.resolution)
        self.board.fill(BLACK)
        self.draw_grid()

    def draw_grid(self):
        for x in range(0, self.resolution[0], self.tile_size):
            for y in range(0, self.resolution[1], self.tile_size):
                rect = pygame.Rect(x, y, self.tile_size, self.tile_size)
                pygame.draw.rect(self.board, WHITE, rect, 1)

    def update(self):
        self.board.fill(BLACK)
        self.draw_grid()
        self.snake.draw(self.board)
        self.apple.draw(self.board)

