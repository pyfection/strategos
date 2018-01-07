

import os

from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from . import assets


class View(Widget):
    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'view.kv')
        Builder.load_file(kv_path)
        super().__init__()

    def add_tile(self, c_tile):
        Tile = assets.tiles[c_tile.type]
        tile = Tile(
            pos=(c_tile.x, c_tile.y),
        )
        self.ids.map.add_widget(tile)
        print('added tile', tile, c_tile.x, c_tile.y)
