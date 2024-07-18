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
        self.board = pygame.display.set_mode(self.resolution)
        self.board.fill(BLACK)
        self.drawGrid()
        
    def drawGrid(self):
        for x in range(0,self.resolution[0],self.blocksize):
            for y in range(0,self.resolution[1],self.blocksize):
                print((x,y))
                rect = pygame.Rect(x,y,self.blocksize,self.blocksize)
                pygame.draw.rect(self.board,WHITE,rect,1)
                pygame.display.update()
    
    def tileSize(self):
        tileWidth = (self.resolution[0] / self.width) 
        tileHeight = (self.resolution[1] / self.height)
        
        return (int(tileWidth),int(tileHeight))

    
        