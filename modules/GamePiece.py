import pygame
from modules.Board import Board

class GamePiece(pygame.sprite.Sprite):
    def __init__(self,board: Board,screen, gamePos,size, next = None):
        self.gamePos = gamePos
        self.screenPos = board.gameToScreenCord(self.gamePos)
        self.screen = screen
        self.board = board
        self.color = 'green'
        self.size = size
        self.rect = pygame.Rect(self.screenPos[0],self.screenPos[1],size,size)
        if not next:        
            self.next = self
        pygame.draw.rect(screen,self.color,self.rect)
    
    def updatePosInfo(self,newPos): 
        self.gamePos = newPos
        self.screenPos = self.board.gameToScreenCord(newPos)       

class Snake():
    def __init__(self, pos, board: Board):
        self.board = board
        self.head = GamePiece(self.board,self.board.board,pos,self.board.blocksize)
        self.mousepos = self.board.screenToGameCoord(pygame.mouse.get_pos())

    def testCoord(self):        
        mousepos = pygame.mouse.get_pos()
        mousepos = self.board.screenToGameCoord(mousepos)
        if mousepos != self.head.gamePos and pygame.mouse.get_focused():
            print(mousepos)
            self.head.updatePosInfo(mousepos)
            self.head.rect.update((self.head.screenPos),(self.head.size,self.head.size))
            
            pygame.draw.rect(self.board.board,self.head.color,self.head.rect)

        
    
    
    