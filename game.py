
import pygame
import sys
from modules.Board import Board

def runGame():
    pygame.init()
    gameBoard = Board((400,400),(20,20))
    while True:
        print('in while')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
    
if __name__ == "__main__":
    runGame()