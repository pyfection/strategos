

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
    'forest': lambda **kwargs: tile_factory("forest.png", **kwargs),
    'hill': lambda **kwargs: tile_factory("hill.png", **kwargs),
    'mountain': lambda **kwargs: tile_factory("mountain.png", **kwargs),
    'wood_bridge': lambda **kwargs: tile_factory("wood_bridge.png", **kwargs),
    'river': lambda **kwargs: tile_factory("river.png", **kwargs),
}
Troop = lambda pos, **kwargs: Image(
    source=os.path.join(ASSET_PATH, "troop.png"),
    size_hint=(None, None),
    size=(SIZE_MOD, SIZE_MOD),
    pos=(pos[0] * SIZE_MOD, pos[1] * SIZE_MOD,),
    **kwargs
)
Target = lambda pos, **kwargs: Image(
    source=os.path.join(ASSET_PATH, "target.png"),
    size_hint=(None, None),
    size=(SIZE_MOD, SIZE_MOD),
    pos=(pos[0] * SIZE_MOD, pos[1] * SIZE_MOD,),
    color=[1, 1, 1, 1],
    **kwargs
)
