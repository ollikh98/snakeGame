import pygame

# from GamePiece import Snake, Apple

BLACK = (0,0,0)
WHITE = (200,200,200)

class Board:
    def __init__(self,resolution, map_size):
        self.resolution = resolution
        self.width = map_size[0]
        self.height = map_size[1]
        self.blocksize, _ = self.tileSize()
        self.map = self.makeMapCoord()
        self.board = pygame.display.set_mode(self.resolution)
        self.board.fill(BLACK)
        self.drawGrid()
        
    def drawGrid(self):
        for x in range(0,self.resolution[0],self.blocksize):
            for y in range(0,self.resolution[1],self.blocksize):
                rect = pygame.Rect(x,y,self.blocksize,self.blocksize)
                pygame.draw.rect(self.board,WHITE,rect,1)
                pygame.display.update()
    
    def tileSize(self):
        tileWidth = (self.resolution[0] / self.width) 
        tileHeight = (self.resolution[1] / self.height)
        
        return (int(tileWidth),int(tileHeight))
        
    def makeMapCoord(self):
        row = 0
        col = 0
        rowDict = {} 
        colDict = {}
        for x in range(0,self.resolution[0],self.blocksize):
            rowDict[range(x,x+self.blocksize)] =  (row,x)
            row +=1 
            
        for y in range(0,self.resolution[1],self.blocksize):
            colDict[range(y,y+self.blocksize)] =  (col,y)
            col += 1 
            
        return (colDict, rowDict)
    
    def screenToGameCoord(self,pos):
        x,y = pos
        gameX = [self.map[0][gamePos] for gamePos in self.map[0] if x in gamePos][0]
        gameY = [self.map[1][gamePos] for gamePos in self.map[1] if y in gamePos][0]
                
        return (gameX,gameY)
    
    
        
        
        