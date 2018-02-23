

import os
from random import Random
from collections import OrderedDict

import ujson

from core.perception.tile import TILE_TYPES
from helpers.convert import pos_to_coord


class MapLoader:
    def __init__(self, map_name, seed):
        self.map_name = map_name
        self.seed = seed
        self.random = Random()

    def get_tile(self, x, y):
        base_x, base_y = x//64, y//64
        self.random.seed(f'{self.seed}-{x}-{y}')

        tile = {'x': x, 'y': y}
        try:
            with open(os.path.join('maps', self.map_name, f'{base_x}|{base_y}.cnk'), 'r') as f:
                json = ujson.load(f)
            coord = pos_to_coord(x, y)
            try:
                tile.update(json[coord])
                tile_type = tile.pop('type')
            except KeyError:
                tile_type = json['default']
        except (FileNotFoundError, KeyError):
            with open(os.path.join('maps', self.map_name, 'default.cnk'), 'r') as f:
                json = ujson.load(f)
            probabilities = sorted(json['probabilities'].items(), key=lambda k: k[1], reverse=True)

            for tile_type, probability in probabilities:
                r = self.random.random()
                if r <= probability:
                    break
            else:
                tile_type = json['default']

        return TILE_TYPES[tile_type], tile
