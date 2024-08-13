import random
from bidict import bidict


def screen_to_game_coord(coord_mapping, pos):
    x, y = pos
    game_x = [coord_mapping[screen_pos] for screen_pos in coord_mapping if x in screen_pos][0]
    game_y = [coord_mapping[screen_pos] for screen_pos in coord_mapping if y in screen_pos][0]

    return game_x, game_y


def game_to_screen_coord(coord_mapping, pos):
    x, y = pos

    screen_x = coord_mapping.inverse[x]
    screen_y = coord_mapping.inverse[y]
    screen_x = screen_x[0]
    screen_y = screen_y[0]

    return screen_x, screen_y


def random_game_pos(coord_mapping):
    grid_size = len(coord_mapping) - 1
    new_x = random.randint(0, grid_size)
    new_y = random.randint(0, grid_size)
    return new_x, new_y


def calc_tile_size(resolution, grid_size):
    width, height = grid_size
    tile_width = int((resolution[0] / width))
    tile_height = int((resolution[1] / height))

    return tile_width, tile_height


def make_coord_mapping(resolution, tile_size):
    # uses bidict to have a key<->key pairing for screen to game coordinates
    grid_pos = 0
    map_dict = {}

    for x in range(0, resolution[0], tile_size):
        map_dict[range(x, x + tile_size)] = grid_pos
        grid_pos += 1

    return bidict(map_dict)
