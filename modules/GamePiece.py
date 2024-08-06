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

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, map: bidict, gamePos, size, color, next=None):
        self.map = map
        self.gamePos = gamePos
        self.screenPos = Utils.gameToScreenCord(self.map, self.gamePos)
        self.color = color
        self.size = size
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], size, size)
        if not next:
            self.next = self

    def updatePosInfo(self, map, newGamePos):
        self.gamePos = newGamePos
        self.screenPos = Utils.gameToScreenCord(map, newGamePos)

    def draw(self, screen):
        self.rect.update(self.screenPos, (self.size, self.size))
        pygame.draw.rect(screen, self.color, self.rect)


    def collisionDetection(self,newX,newY):
        if newX not in self.map.inverse:
            print('attempting to go out of bounds')
            return -1
        if newY not in self.map.inverse:
            print('attempting to go out of bounds')
            return -1

# TODO: restructure board,snake gamepiece link, board should contain all pieces
class Apple(GamePiece):
    def __init__(self, map, size, color):
        super().__init__(map, Utils.generateRandomGamePos(map), size, color)
        self.mapsize = len(map)

    def collected(self, snakePos):
        if snakePos == self.gamePos:
            self.gamePos = Utils.generateRandomGamePos(self.map)
            newX = random.randint(0,self.mapsize)
            newY = random.randint(0,self.mapsize)
            self.gamePos = (newX,newY)
            self.screenPos = Utils.gameToScreenCord(self.gamePos)


class Snake():
    def __init__(self, gameMap, pos, size):
        self.head = GamePiece(gameMap, pos, size, 'green')
        self.body = []
        self.body.append(self.head)
        self.movementTicker = 0
        self.canMove = True
        self.dir = RIGHT
        # self.mousepos = self.board.screenToGameCoord(pygame.mouse.get_pos())


    def move(self):
        keys = pygame.key.get_pressed()
        newX, newY = self.head.gamePos

        if keys[pygame.K_LEFT] and self.dir != RIGHT:
            self.dir = LEFT
        if keys[pygame.K_RIGHT] and self.dir != LEFT:
            self.dir = RIGHT
        if keys[pygame.K_UP] and self.dir != DOWN:
            self.dir = UP
        if keys[pygame.K_DOWN] and self.dir != UP:
            self.dir = DOWN

        # no key pressed and time to move
        if self.movementTicker >= 10:
            self.canMove = True

        if self.canMove:
            newX, newY = tuple(np.add(self.head.gamePos, self.dir))
            self.canMove = False
            self.movementTicker = 0

        self.movementTicker += 1

        collision = self.head.collisionDetection(newX, newY)

        if collision == -1:
            return -1

        newPos = (newX, newY)
        self.head.updatePosInfo(self.head.map, newPos)

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
