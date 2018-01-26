

import os

from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock

from lib.widgets.console import Console
from lib.widgets.tile import Tile
from lib.widgets.overlay import Target
from lib.widgets.troop import Troop


class View(Widget):
    MOVE_ANIM = 'in_out_cubic'
    ANIM_DUR = .7
    SIZE_MOD = 32

    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'view.kv')
        Builder.load_file(kv_path)
        super().__init__()
        self.troops = {}
        self.focus_center = (0, 0)

        self.console = Console(pos=self.pos, height=self.height, width=100, size_hint=(None, None))
        self.target = Target(pos=(0, 0))
        self.target_anim = None

        self.add_widget(self.console)

        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')

        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.bind(size=self.on_size)

        Clock.schedule_once(lambda dt: self.center_camera())

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
        elif keycode[1] == '$':
            self.toggle_console()
        return True

    def on_size(self, inst, value):
        self.center_camera()

    def toggle_console(self):
        pass

    def add_tile(self, c_tile):
        tile = Tile(
            name=c_tile.type,
            pos=(c_tile.x * self.SIZE_MOD, c_tile.y * self.SIZE_MOD),
        )
        self.ids.map.add_widget(tile)
        for troop in self.troops.values():  # ToDo: this is not very performant, find a better solution
            self.ids.map.remove_widget(troop)
            self.ids.map.add_widget(troop)

    def add_troop(self, faction_name, c_troop):
        if c_troop.id in self.troops or not c_troop.units:
            return
        troop = Troop(faction=faction_name, pos=c_troop.pos)
        self.ids.map.add_widget(troop)
        self.troops[c_troop.id] = troop

    def remove_troop(self, troop_id):
        troop = self.troops.pop(troop_id)
        self.ids.map.remove_widget(troop)

    def change_troop_unit_amount(self, troop_id, amount):
        troop = self.troops[troop_id]
        label = Label(text=str(amount), center=troop.center, font_size=25, color=[1, 0, 0, 1])
        self.ids.map.add_widget(label)
        new_center = troop.center[0], troop.center[1] + self.SIZE_MOD
        anim = Animation(center=new_center, font_size=5, color=[1, 0, 0, .5])
        anim.start(label)
        anim.bind(on_complete=lambda animation, widget: self.ids.map.remove_widget(widget))

    def center_camera(self):
        x, y = self.focus_center[0] * self.SIZE_MOD, self.focus_center[1] * self.SIZE_MOD
        x, y = self.ids.map.x + x, self.ids.map.y + y
        offsetx = x - self.center[0]
        offsety = y - self.center[1]
        fx = self.ids.map.center[0] - offsetx
        fy = self.ids.map.center[1] - offsety
        # self.ids.map.center = (fx, fy)
        anim = Animation(x=fx, y=fy, duration=self.ANIM_DUR, t=self.MOVE_ANIM)
        anim.start(self.ids.map)

    def move_troop(self, troop_id, x, y):
        try:
            troop = self.troops[troop_id]
        except KeyError:
            return
        pos = (x * self.SIZE_MOD, y * self.SIZE_MOD)
        anim = Animation(x=pos[0], y=pos[1], duration=self.ANIM_DUR, t=self.MOVE_ANIM)
        anim.start(troop)

    def set_target(self, x, y):
        if self.target_anim:
            self.target_anim.cancel(self.target)
        self.ids.map.remove_widget(self.target)
        pos = (x * self.SIZE_MOD, y * self.SIZE_MOD)
        self.target.pos = pos
        self.target.color = [1, 1, 1, 1]
        self.ids.map.add_widget(self.target)

    def move_target(self, x, y):
        pos = (x * self.SIZE_MOD, y * self.SIZE_MOD)
        self.ids.map.remove_widget(self.target)
        self.ids.map.add_widget(self.target)
        self.target.color = [1, 1, 1, 1]
        self.target_anim = Animation(pos=pos, duration=self.ANIM_DUR, t=self.MOVE_ANIM)
        self.target_anim.start(self.target)

    def unset_target(self):
        anim = Animation(color=[1, 1, 1, 0], duration=self.ANIM_DUR)
        anim.start(self.target)
        anim.bind(on_complete=lambda animation, widget: self.ids.map.remove_widget(widget))
