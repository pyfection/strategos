

import os

from PIL import Image
import json

from core.tile import TILE_TYPES


def load_map(map_name):
    image = Image.open(os.path.join('maps', map_name) + '.png')
    pixels = image.load()
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b = pixels[x, y]
            hex = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

            for TileType in TILE_TYPES.values():
                if TileType.color == hex:
                    yield TileType(x, y)


def load_game(game_name):
    path = os.path.join('saves', game_name + '.gs')
    with open(path, 'r') as f:
        content = f.read()
    return json.loads(content)

