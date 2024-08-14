import pygame
import numpy as np
from random import choice
import bidict
from modules import Utils

# DIRECTION CONSTANTS
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
STILL = (0, 0)
POSSIBLE_DIRECTIONS = [UP,DOWN,LEFT,RIGHT]
OPPOSING_DIRECTIONS = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


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
        collision = self.detect_collision()
        if collision:
            return True
        self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, self.game_pos)

    def draw(self, screen):
        self.rect.update(self.screen_pos, (self.size, self.size))
        pygame.draw.rect(screen, self.color, self.rect, 5)

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

    def collected(self, head_pos, occupied_tiles):
        if head_pos == self.game_pos:
            self.game_pos = Utils.random_game_pos(self.coord_mapping)
            while self.game_pos in occupied_tiles:
                apple_pos_error = f"attempted apple in snake: {self.game_pos}"
                print(apple_pos_error)
                self.game_pos = Utils.random_game_pos(self.coord_mapping)
            self.screen_pos = Utils.game_to_screen_coord(self.coord_mapping, self.game_pos)
            return True
        return False


class Snake:
    def __init__(self, coord_mapping, pos, size):
        self.head = GamePiece(coord_mapping, pos, size, 'blue')
        self.body = []
        self.body.append(self.head)
        self.movement_ticker = 0
        self.moved = False
        self.occupied_tiles = []
        self.occupied_tiles.append(self.head.game_pos)

    def extend(self):
        # TODO: fix error where new tile crashes game because it tries to spawn outside of board
        last_piece = self.body[-1]
        direction = last_piece.direction
        tried_directions = []
        new_piece_pos = tuple(np.subtract(last_piece.game_pos, last_piece.direction))
        new_piece_pos = (int(new_piece_pos[0]),int(new_piece_pos[1]))
        print(new_piece_pos)
        while new_piece_pos[0] not in last_piece.coord_mapping.inverse or \
                new_piece_pos[1] not in last_piece.coord_mapping.inverse:

            tried_directions.append(direction)
            direction = choice(POSSIBLE_DIRECTIONS)
            if direction in tried_directions:
                continue
            new_piece_pos = tuple(np.subtract(last_piece.game_pos, direction))
            print('new direction')
            print(new_piece_pos)

        new_piece = GamePiece(last_piece.coord_mapping, new_piece_pos, last_piece.size, color='green',
                              direction=direction)
        self.body[-1].next = new_piece
        self.body.append(new_piece)
        self.occupied_tiles.append(new_piece_pos)

    def slither(self):

        # TODO: by pressing keys fast oen can reverse direction without intermediate step.
        #  set up logic so that one has to move to next coord before next step is allowed
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
            return True

        self.moved = False
        self.occupied_tiles = []
        for piece in self.body[::-1]:
            collision = piece.move()
            if collision:
                return False
            if piece.next:
                piece.next.direction = piece.direction
            self.occupied_tiles.append(piece.game_pos)
        self.movement_ticker = 0

        return True

    def collision(self):
        return self.head.detect_collision()

    def draw(self, screen):
        for part in self.body:
            part.draw(screen)
        self.moved = True
