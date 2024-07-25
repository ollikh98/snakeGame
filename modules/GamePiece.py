import pygame
from modules.Board import Board

class GamePiece(pygame.sprite.Sprite):
    def __init__(self,board, posInfo,size,color):
        self.rect = pygame.Rect(posInfo[0][1],posInfo[1][1],size,size)
        pygame.draw.rect(board,color,self.rect)
         
 #TODO: RESTRCTURE SNAKE AND GAMEPIECE, MOVE INTERNALS FROM SNAKE TO GAMEPIECE       

class Snake():
    def __init__(self, pos, board: Board):
        self.board = board
        self.bodysize = self.board.blocksize
        self.posInfo = self.board.screenToGameCoord(pos)
        self.boardPos = (self.posInfo[0][0],self.posInfo[1][0])
        self.screenPos = (self.posInfo[0][1],self.posInfo[1][1])
        self.color = 'green'
        self.head = GamePiece(self.board.board,self.posInfo,self.bodysize,self.color)
        self.mousepos = self.board.screenToGameCoord(pygame.mouse.get_pos())
        self.head.update(pos[0],pos[1])
        
    
    def updatePosInfo(self,newInfo): 
        self.posInfo = newInfo
        self.boardPos = (self.posInfo[0][0],self.posInfo[1][0])
        self.screenPos = (self.posInfo[0][1],self.posInfo[1][1])
        
    def testCoord(self):        
        mousepos = pygame.mouse.get_pos()
        mousepos = self.board.screenToGameCoord(mousepos)
        if mousepos != self.posInfo:
            self.updatePosInfo(mousepos)
            self.head.rect.update((self.screenPos),(self.bodysize,self.bodysize))
            
            pygame.draw.rect(self.board.board,self.color,self.head.rect)
                
    def testUpdateOnHover(self):
        mousepos = pygame.mouse.get_pos()
        mouseposGame = self.board.screenToGameCoord(mousepos)
        
        if mouseposGame != self.mousepos:
            print(mouseposGame)
            self.board.makeMapCoord()
            self.mousepos = mouseposGame


        
    
    
    