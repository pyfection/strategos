

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__name__)))
from collections import Counter

import ujson
from PIL import Image

from helpers.convert import pos_to_coord


COLORS_MAPPING = {
    '#3b7c27': 'grass',
    '#1c3c16': 'forest',
    '#928f34': 'hill',
    '#586069': 'mountain',
    '#966a44': 'wood_bridge',
    '#1886ab': 'river',
}

image_name, map_name = sys.argv[1:3]

image = Image.open(os.path.join('maps', image_name) + '.png')
pixels = image.load()
chunks = {}

for x in range(image.size[0]):
    for y in range(image.size[1]):
        r, g, b = pixels[x, y]
        y = image.size[1] - 1 - y
        hex = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)
        tile_type = COLORS_MAPPING[hex]
        chunk_coord = pos_to_coord(x//64, y//64)
        coord = pos_to_coord(x, y)
        chunks.setdefault(chunk_coord, {})
        chunks[chunk_coord][coord] = {
            'type': tile_type,
        }

for coord, content in chunks.items():
    occurrences = Counter([c['type'] for c in content.values()])
    tile_type = occurrences.most_common(1)[0][0]
    for tile_coord, tile in list(content.items()):
        if tile['type'] == tile_type:
            content.pop(tile_coord)
    content['default'] = tile_type

    with open(os.path.join('maps', map_name, f'{coord}.cnk'), 'w') as f:
        f.write(ujson.dumps(content, indent=2))
