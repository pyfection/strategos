

import json
import os

from PIL import Image

from core.perception.tile import TILE_TYPES
from helpers.convert import pos_to_coord


def load_map(map_name):
    image = Image.open(os.path.join('maps', map_name) + '.png')
    pixels = image.load()
    result = {}
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            r, g, b = pixels[x, y]
            hex = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

            for TileType in TILE_TYPES.values():
                if TileType.color == hex:
                    result[pos_to_coord(x, image.size[1]-1-y)] = {
                        'type': TileType.type,
                    }
                    break
    return result


def load_game(game_name):
    path = os.path.join('saves', game_name + '.gs')
    with open(path, 'r') as f:
        content = f.read()
    return json.loads(content)


def save_game(game, game_name):
    path = os.path.join('saves', game_name + '.gs')
    content = json.dumps(game)
    with open(path, 'w') as f:
        f.write(content)
