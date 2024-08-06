import pygame
from modules.GamePiece import Snake, Apple

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

# Board keeps track of active pieces, and drawing/frame updates
class Board:
    def __init__(self, map, resolution, map_size, tilesize, snake: Snake, apple: Apple):
        self.resolution = resolution
        self.width = map_size[0]
        self.height = map_size[1]
        self.snake = snake
        self.apple = apple
        self.tilesize = tilesize
        self.map = map
        self.board = pygame.display.set_mode(self.resolution)
        self.board.fill(BLACK)
        self.drawGrid()


    def drawGrid(self):
        for x in range(0, self.resolution[0], self.tilesize):
            for y in range(0, self.resolution[1], self.tilesize):
                rect = pygame.Rect(x, y, self.tilesize, self.tilesize)
                pygame.draw.rect(self.board, WHITE, rect, 1)

    def updateFrame(self):
        self.board.fill(BLACK)
        self.drawGrid()
        self.snake.head.draw(self.board)
