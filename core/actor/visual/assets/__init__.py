

import os

from kivy.uix.image import Image


ASSET_PATH = os.path.dirname(__file__)
SIZE_MOD = 32


def tile_factory(file_name, pos, **kwargs):
    pos = pos[0] * SIZE_MOD, pos[1] * SIZE_MOD
    return Image(
        source=os.path.join(ASSET_PATH, "tiles", file_name),
        size_hint=(None, None),
        size=(SIZE_MOD, SIZE_MOD),
        pos=pos,
        **kwargs
    )


tiles = {
    'grass': lambda **kwargs: tile_factory("grass.png", **kwargs),
    'settlement': lambda **kwargs: tile_factory("settlement.png", **kwargs),
}
Troop = lambda pos, **kwargs: Image(
    source=os.path.join(ASSET_PATH, "troop.png"),
    size_hint=(None, None),
    size=(SIZE_MOD, SIZE_MOD),
    pos=(pos[0] * SIZE_MOD, pos[1] * SIZE_MOD,),
    **kwargs
)
