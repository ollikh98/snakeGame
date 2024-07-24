
import pygame
import sys
from modules.Board import Board
from modules.GamePiece import Snake

def runGame():
    pygame.init()
    snake = Snake(200,200)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
if __name__ == "__main__":
    runGame()