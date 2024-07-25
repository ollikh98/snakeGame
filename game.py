
import pygame
import sys
from modules.Board import Board
from modules.GamePiece import Snake

def runGame():
    pygame.init()
    board = Board((400,400),(10,10))
    snake = Snake((5,5),board)
    while True:
        snake.testCoord()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
if __name__ == "__main__":
    runGame()