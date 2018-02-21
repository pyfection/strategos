

import os
from collections import OrderedDict

from PIL import Image

from core.perception.tile import TILE_TYPES


class MapLoader:
    def __init__(self, map_name):
        self.map_name = map_name
        self.pixels_buffer = OrderedDict()
        self.pixels_buffer_max_len = 6

    def get_tile(self, x, y):
        base_x, base_y = int(x - x % 64), int(y - y % 64)
        try:
            pixels = self.pixels_buffer[(base_x, base_y)]
            self.pixels_buffer.move_to_end((base_x, base_y))
        except KeyError:
            try:
                image = Image.open(os.path.join('maps', self.map_name, f'{base_x}|{base_y}') + '.png')
            except FileNotFoundError:
                return None
            pixels = image.load()
            self.pixels_buffer[(base_x, base_y)] = pixels
            if len(self.pixels_buffer) > self.pixels_buffer_max_len:
                self.pixels_buffer.popitem(last=False)

        r, g, b = pixels[x%64, 63-y%64]
        hex = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        for TileType in TILE_TYPES.values():
            if TileType.color == hex:
                return TileType, (x, y)

        return None
