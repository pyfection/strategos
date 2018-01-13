

import os

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget

from . import assets


class View(Widget):
    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'view.kv')
        Builder.load_file(kv_path)
        self.troops = {}
        self.focus_center = (0, 0)
        super().__init__()
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.bind(size=self.on_size)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'right':
            self.ids.map.x -= 10
        elif keycode[1] == 'left':
            self.ids.map.x += 10
        elif keycode[1] == 'up':
            self.ids.map.y -= 10
        elif keycode[1] == 'down':
            self.ids.map.y += 10
        return True

    def on_size(self, inst, value):
        self.center_camera()

    def add_tile(self, c_tile):
        Tile = assets.tiles[c_tile.type]
        tile = Tile(
            pos=(c_tile.x, c_tile.y),
        )
        self.ids.map.add_widget(tile)
        for troop in self.troops.values():  # ToDo: this is not very performant, find a better solution
            self.ids.map.remove_widget(troop)
            self.ids.map.add_widget(troop)

    def add_troop(self, c_troop):
        troop = assets.Troop((c_troop.x, c_troop.y))
        self.ids.map.add_widget(troop)
        self.troops[c_troop.id] = troop

    def center_camera(self):
        x, y = self.focus_center[0] * assets.SIZE_MOD, self.focus_center[1] * assets.SIZE_MOD
        x, y = self.ids.map.x + x, self.ids.map.y + y
        offsetx = x - self.center[0]
        offsety = y - self.center[1]
        fx = self.ids.map.center[0] - offsetx
        fy = self.ids.map.center[1] - offsety
        self.ids.map.center = (fx, fy)

    def move_troop(self, troop_id, x, y):
        troop = self.troops[troop_id]
        pos = (x * assets.SIZE_MOD, y * assets.SIZE_MOD)
        troop.pos = pos
