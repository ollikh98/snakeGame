import pygame
import numpy as np
from modules.Board import Board
from copy import deepcopy

# DIRECTION CONSTANTS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class GamePiece(pygame.sprite.Sprite):
    def __init__(self, board: Board, screen, gamePos, size, next=None):
        self.gamePos = gamePos
        self.screenPos = board.gameToScreenCord(self.gamePos)
        self.screen = screen
        self.dir = LEFT
        self.board = board
        self.color = 'green'
        self.size = size
        self.canMove = True
        self.movementTicker = 0
        self.rect = pygame.Rect(self.screenPos[0], self.screenPos[1], size, size)
        if not next:
            self.next = self
        pygame.draw.rect(screen, self.color, self.rect)

    def updatePosInfo(self, newGamePos):
        self.gamePos = newGamePos
        self.screenPos = self.board.gameToScreenCord(newGamePos)

    def draw(self):
        self.rect.update(self.screenPos, (self.size, self.size))
        pygame.draw.rect(self.board.board, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        prevX, prevY = self.gamePos
        newX, newY = self.gamePos

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
            newX, newY = tuple(np.add(self.gamePos, self.dir))
            self.canMove = False
            self.movementTicker = 0

        self.movementTicker += 1

        if newX not in self.board.map.inverse:
            newX = prevX
            print('attempting to go out of bounds')
        if newY not in self.board.map.inverse:
            newY = prevY
            print('attempting to go out of bounds')

        newPos = (newX, newY)
        self.updatePosInfo(newPos)
        self.board.updateFrame()
        self.draw()


class Snake():
    def __init__(self, pos, board: Board):
        self.board = board
        self.head = GamePiece(self.board, self.board.board, pos, self.board.blocksize)
        self.mousepos = self.board.screenToGameCoord(pygame.mouse.get_pos())

    def testCoord(self):
        mousepos = pygame.mouse.get_pos()
        mousepos = self.board.screenToGameCoord(mousepos)
        if mousepos != self.head.gamePos and pygame.mouse.get_focused():
            self.head.updatePosInfo(mousepos)
            self.board.updateFrame()
            self.head.draw()
