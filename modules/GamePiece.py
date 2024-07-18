import pygame

class GamePiece(pygame.Rect):
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        