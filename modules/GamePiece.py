import pygame
import numpy as np
from random import randint
import bidict
from modules import Utils

# DIRECTION CONSTANTS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STILL = (0, 0)


class GamePiece(pygame.sprite.Sprite):
    def __init__(self, coord_mapping: bidict, game_pos: tuple, size: int, color: str, direction: tuple = STILL):
        self.coord_mapping = coord_mapping
        self.grid_size = len(coord_mapping)
        self.game_pos = game_pos
        self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, self.game_pos)
        self.color = color
        self.size = size
        self.rect = pygame.Rect(self.screen_pos[0], self.screen_pos[1], size, size)
        self.next = None
        self.direction = direction

    def update(self, new_pos):
        self.game_pos = new_pos
        self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, new_pos)

    def move(self):
        new_pos = tuple(np.add(self.game_pos, self.direction))
        self.game_pos = new_pos
        self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, self.game_pos)

    def draw(self, screen):
        self.rect.update(self.screen_pos, (self.size, self.size))
        pygame.draw.rect(screen, self.color, self.rect)

    def detect_collision(self):
        if (self.game_pos[0] not in self.coord_mapping.inverse) or (self.game_pos[1] not in self.coord_mapping.inverse):
            print('attempting to go out of bounds')
            return True

    def __str__(self):
        return (
            f' Gamepiece attributes: \n'
            f' coord_mapping: {self.coord_mapping} \n'
            f' game_pos: {self.game_pos} \n'
            f' screen_pos: {self.screen_pos} \n'
            f' color: {self.color} \n'
            f' size: {self.size} \n'
            f' direction: {self.direction} \n'
        )


class Apple(GamePiece):
    def __init__(self, coord_mapping, size, color):
        super().__init__(coord_mapping, Utils.random_game_pos(coord_mapping), size, color)

    def collected(self, head_pos):
        # TODO: write logic so that apple can't spawn inside snake
        if head_pos == self.game_pos:
            self.game_pos = Utils.random_game_pos(self.coord_mapping)
            self.game_pos = (randint(0, self.grid_size - 1), randint(0, self.grid_size - 1))
            self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, self.game_pos)
            return True
        return False


class Snake:
    def __init__(self, coord_mapping, pos, size):
        self.head = GamePiece(coord_mapping, pos, size, 'green')
        self.body = []
        self.body.append(self.head)
        self.movement_ticker = 0
        self.moved = False

    def extend(self):
        last_piece = self.body[-1]
        new_piece_pos = tuple(np.subtract(last_piece.game_pos, last_piece.direction))
        new_piece = GamePiece(last_piece.coord_mapping, new_piece_pos, last_piece.size, color='green',
                              direction=last_piece.direction)
        self.body[-1].next = new_piece
        self.body.append(new_piece)

    def move(self):

        # TODO: by pressing keys fast oen can reverse direction without intermediate step.
        #  set up logic so that oen has to move to next coord before next step is allowed
        self.movement_ticker += 1

        keys = pygame.key.get_pressed()

        if self.moved:
            if keys[pygame.K_LEFT] and self.head.direction != RIGHT:
                self.head.direction = LEFT
            if keys[pygame.K_RIGHT] and self.head.direction != LEFT:
                self.head.direction = RIGHT
            if keys[pygame.K_UP] and self.head.direction != DOWN:
                self.head.direction = UP
            if keys[pygame.K_DOWN] and self.head.direction != UP:
                self.head.direction = DOWN

        # TODO: set movement_ticker as a function of map size, find reasonable function
        if self.movement_ticker < 20:
            return

        self.moved = False
        for piece in self.body[::-1]:
            piece.move()
            if piece.next:
                piece.next.direction = piece.direction
        self.movement_ticker = 0

    def collision(self):
        return self.head.detect_collision()

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)
        self.moved = True
