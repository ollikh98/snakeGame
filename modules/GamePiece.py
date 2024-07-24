import pygame
from modules.Board import Board

class GamePiece():
    def __init__(self, xpos, ypos):
        self.pos = pygame.Vector2(xpos,ypos)
        self.next = self
        

class Snake():
    def __init__(self, xpos, ypos):
        self.board = Board((400,400),(20,20))
        self.head = GamePiece(xpos,ypos)
        self.color = 'green'
        self.startpos = (0,0)
        self.body = pygame.Rect(310,290,self.board.blocksize, self.board.blocksize)
        print(type(self.body))
        pygame.draw.rect(self.board.board,self.color,self.body,self.board.blocksize)

        
    
    
    