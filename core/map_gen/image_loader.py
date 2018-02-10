

import os
from collections import OrderedDict

from PIL import Image

from core.tile import TILE_TYPES, Grass


class ImageLoader:
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
            image = Image.open(os.path.join('maps', self.map_name, f'{base_x}_{base_y}') + '.png')
            pixels = image.load()
            self.pixels_buffer[(base_x, base_y)] = pixels
            if len(self.pixels_buffer) > self.pixels_buffer_max_len:
                self.pixels_buffer.popitem(last=False)

        r, g, b = pixels[x, y]
        hex = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        for TileType in TILE_TYPES.values():
            if TileType.color == hex:
                return TileType(x, y)

        return Grass(x, y)
