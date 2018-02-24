

import os

from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from visual.building import Settlement
from visual.overlay import Target, MapMode
from visual.tile import Tile
from visual.troop import Troop

from helpers.maths import distance
from visual.console import Console
from helpers.convert import pos_to_coord


class View(Widget):
    MOVE_ANIM = 'in_out_cubic'
    REVEAL_TILE_ANIM = 'in_quart'
    FOW_ANIM = 'in_cubic'
    ANIM_DUR = .7
    SIZE_MOD = 32

    def __init__(self, actor):
        kv_path = os.path.join(os.path.dirname(__file__), 'view.kv')
        Builder.load_file(kv_path)
        super().__init__()
        self.actor = actor
        self.troops = {}
        self.tiles = {}
        self.map_modes = {
            'faction': {}
        }
        self.current_map_mode = None
        self.focus_center = (0, 0)
        self.focus_radius = 5

        self.console = Console(pos=self.pos, height=self.height, width=100, size_hint=(None, None))
        self.console.commands['exit'] = self.toggle_console
        self.console.commands['spawn_troop'] = self.actor.spawn_troop
        self.target = Target(pos=(0, 0))
        self.target_anim = None

        self.bind(size=self.on_size)
        self.console.ids.input.bind(focus=self._con_open_keyboard)

        self._open_keyboard()

        Clock.schedule_once(lambda dt: self.center_camera())

    def _con_open_keyboard(self, inst, value):
        if value is False:
            self._open_keyboard()

    def _open_keyboard(self):
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text')

        self._keyboard.bind(on_key_down=self._on_keyboard_down)

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
        elif keycode[1] == 'f':
            self.toggle_map_mode('faction')
        elif keycode[1] == '$':
            self.toggle_console()
        return True

    def _ensure_troops_on_top(self):
        for troop in self.troops.values():  # ToDo: this is not very performant, find a better solution
            self.ids.map.remove_widget(troop)
            self.ids.map.add_widget(troop)

    def on_size(self, inst, value):
        self.center_camera()

    def toggle_console(self):
        if self.console in self.children:
            self.remove_widget(self.console)
        else:
            self.add_widget(self.console)
            self.console.ids.input.focus = True

    def toggle_map_mode(self, mode_type):
        if self.current_map_mode:
            modes = self.map_modes[self.current_map_mode].values()
            for mode in modes:
                self.ids.map.remove_widget(mode)

        if self.current_map_mode == mode_type:
            self.current_map_mode = None
        else:
            modes = self.map_modes[mode_type].values()
            for mode in modes:
                self.ids.map.add_widget(mode)
            self.current_map_mode = mode_type
            self._ensure_troops_on_top()

    @mainthread
    def add_tile(self, c_tile):
        tx, ty = c_tile.x * self.SIZE_MOD, c_tile.y * self.SIZE_MOD
        sx, sy = tx + int(self.SIZE_MOD / 2), ty + int(self.SIZE_MOD / 2)
        tile = Tile(
            name=c_tile.type,
            pos=(sx, sy),
            size=(0, 0)
        )
        self.tiles[(c_tile.x, c_tile.y)] = tile
        self.ids.map.add_widget(tile)
        anim = Animation(
            x=tx, y=ty, width=self.SIZE_MOD, height=self.SIZE_MOD, duration=self.ANIM_DUR, t=self.REVEAL_TILE_ANIM
        )
        if c_tile.population > 0:
            try:
                faction = c_tile.owner.faction.name
            except AttributeError:
                faction = 'default'
            settlement = Settlement(
                faction=faction,
                size=c_tile.population,
                pos=(sx, sy),
                width=0,
                height=0
            )
            self.ids.map.add_widget(settlement)
            anim.start(settlement)
        anim.start(tile)

        try:
            faction = c_tile.dominion.ruler.faction
        except AttributeError:
            pass
        else:
            color = [0, 0, .5, .5]  # ToDo: make this color faction specific
            map_mode = MapMode(pos=(tx, ty), color=color)
            self.map_modes['faction'][(c_tile.x, c_tile.y)] = map_mode

        self._ensure_troops_on_top()

    @mainthread
    def add_troop(self, faction_name, c_troop):
        if c_troop.id in self.troops or not c_troop.units:
            return
        tx, ty = c_troop.x * self.SIZE_MOD, c_troop.y * self.SIZE_MOD
        sx, sy = tx + int(self.SIZE_MOD / 2), ty + int(self.SIZE_MOD / 2)
        troop = Troop(
            faction=faction_name or 'default',
            pos=(sx, sy),
            width=0,
            height=0
        )
        self.ids.map.add_widget(troop)
        self.troops[c_troop.id] = troop
        anim = Animation(
            x=tx, y=ty, width=self.SIZE_MOD, height=self.SIZE_MOD, duration=self.ANIM_DUR, t=self.REVEAL_TILE_ANIM
        )
        anim.start(troop)

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
        self.ids.current_pos.text = pos_to_coord(*self.focus_center)
        x, y = self.focus_center[0] * self.SIZE_MOD, self.focus_center[1] * self.SIZE_MOD
        x, y = self.ids.map.x + x, self.ids.map.y + y
        offsetx = x - self.center[0]
        offsety = y - self.center[1]
        fx = self.ids.map.center[0] - offsetx
        fy = self.ids.map.center[1] - offsety
        # self.ids.map.center = (fx, fy)
        anim = Animation(x=fx, y=fy, duration=self.ANIM_DUR, t=self.MOVE_ANIM)
        anim.start(self.ids.map)

        for pos, tile in list(self.tiles.items()):
            in_range = distance(pos, self.focus_center) <= self.focus_radius
            if in_range and tile.color != [1, 1, 1, 1]:
                anim = Animation(color=[1, 1, 1, 1], duration=self.ANIM_DUR, t=self.FOW_ANIM)
                anim.start(tile)
            elif not in_range and tile.color == [1, 1, 1, 1]:
                anim = Animation(color=[.7, .7, .7, .7], duration=self.ANIM_DUR, t=self.FOW_ANIM)
                anim.start(tile)

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
