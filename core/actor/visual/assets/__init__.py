

import os

from kivy.uix.image import Image


ASSET_PATH = os.path.dirname(__file__)


def tile_factory(file_name, pos, **kwargs):
    pos = pos[0] * 32, pos[1] * 32
    return Image(
        source=os.path.join(ASSET_PATH, "tiles", file_name),
        size_hint=(None, None),
        size=(32, 32),
        pos=pos,
        **kwargs
    )


tiles = {
    'grass': lambda **kwargs: tile_factory("grass.png", **kwargs),
    'settlement': lambda **kwargs: tile_factory("settlement.png", **kwargs),
}
