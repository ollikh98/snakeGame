import pygame
import numpy as np
import random
import bidict
from modules import Utils
from copy import deepcopy

# DIRECTION CONSTANTS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STILL = (0, 0)

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, map: bidict, gamePos, size, color, dir=STILL):
        self.map = map
        self.gamePos = gamePos
        self.screenPos = Utils.gameToScreenCord(self.map, self.gamePos)
        self.color = color
        self.size = size
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], size, size)
        self.next = None
        self.dir = dir
        self.prevDir = dir

    def updatePosInfo(self,newGamePos):
        self.gamePos = newGamePos
        self.screenPos = Utils.gameToScreenCord(self.map, newGamePos)

    def movePiece(self):
        newPos = tuple(np.add(self.gamePos,self.dir))
        self.gamePos = newPos
        self.screenPos = Utils.gameToScreenCord(self.map,self.gamePos)

    def getGamePos(self):
        return self.gamePos

    def draw(self, screen):
        self.rect.update(self.screenPos, (self.size, self.size))
        pygame.draw.rect(screen, self.color, self.rect)

    def __str__(self):
        return (
            f' Gamepiece attributes: \n'
            f' map: {self.map} \n'
            f' gamePos: {self.gamePos} \n'
            f' screenPos: {self.screenPos} \n'
            f' color: {self.color} \n'
            f' size: {self.size} \n'
            f' dir: {self.dir} \n'
        )

    def collisionDetection(self,newX,newY):
        if newX not in self.map.inverse:
            print('attempting to go out of bounds')
            return -1
        if newY not in self.map.inverse:
            print('attempting to go out of bounds')
            return -1

class Apple(GamePiece):
    def __init__(self, map, size, color):
        super().__init__(map, Utils.generateRandomGamePos(map), size, color)
        self.mapsize = len(map)

    def collected(self, snakePos):
        if snakePos == self.gamePos:
            self.gamePos = Utils.generateRandomGamePos(self.map)
            newX = random.randint(0, self.mapsize-1)
            newY = random.randint(0, self.mapsize-1)
            self.gamePos = (newX,newY)
            self.screenPos = Utils.gameToScreenCord(self.map, self.gamePos)
            return True
        return False


class Snake():
    def __init__(self, gameMap, pos, size):
        self.head = GamePiece(gameMap, pos, size, 'green')
        self.body = []
        self.body.append(self.head)
        self.movementTicker = 0
        self.canMove = False
        # self.mousepos = self.board.screenToGameCoord(pygame.mouse.get_pos())


    def addBody(self):
        lastPiece = self.body[-1]
        newPos = tuple(np.subtract(lastPiece.gamePos, lastPiece.dir))
        newPiece = GamePiece(lastPiece.map, newPos, lastPiece.size, color='green', dir=lastPiece.dir)
        self.body[-1].next = newPiece
        self.body.append(newPiece)
    def move(self):

        keys = pygame.key.get_pressed()
        self.head.prevDir = self.head.dir
        if keys[pygame.K_LEFT] and self.head.dir != RIGHT:
            self.head.dir = LEFT
        if keys[pygame.K_RIGHT] and self.head.dir != LEFT:
            self.head.dir = RIGHT
        if keys[pygame.K_UP] and self.head.dir != DOWN:
            self.head.dir = UP
        if keys[pygame.K_DOWN] and self.head.dir != UP:
            self.head.dir = DOWN

        # no key pressed and time to move
        if self.movementTicker >= 20:
            self.canMove = True

        if self.canMove:
            for piece in self.body[::-1]:
                piece.movePiece()
                if piece.next:
                    piece.next.dir = piece.dir
            self.canMove = False
            self.movementTicker = 0

        self.movementTicker += 1

        headX, headY = self.head.gamePos
        collision = self.head.collisionDetection(headX, headY)

        if collision == -1:
            return -1

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)


    def testCoord(self):
        mousepos = pygame.mouse.get_pos()
        mousepos = self.board.screenToGameCoord(mousepos)
        if mousepos != self.head.gamePos and pygame.mouse.get_focused():
            self.head.updatePosInfo(mousepos)
            self.board.updateFrame()
            self.head.draw()
