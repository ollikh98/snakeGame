import pygame
from bidict import bidict

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
        #uses bidict to have a key<->key pairing for screen to game coordinates
        gridPos = 0
        mapDict = {}
        
        for x in range(0,self.resolution[0],self.blocksize):
            mapDict[range(x,x+self.blocksize)] =  gridPos
            gridPos +=1 
            
        return bidict(mapDict)
        
    def screenToGameCoord(self,pos):
        x,y = pos
        gameX = [self.map[screenPos] for screenPos in self.map if x in screenPos][0]
        gameY = [self.map[screenPos] for screenPos in self.map if y in screenPos][0]
        
        return(gameX,gameY)
    
    def gameToScreenCord(self,pos):
        x,y = pos
        
        screenX = self.map.inverse[x]
        screenY = self.map.inverse[y]
        screenX = screenX[0]
        screenY = screenY[0]
        
        return (screenX,screenY)
    
        
        
        