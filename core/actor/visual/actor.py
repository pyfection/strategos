

from time import time, sleep

from kivy.app import App
from kivy.core.window import Window

from core.event import Quit
from core.actor.actor import Actor
from .view import View
from . import assets


class Visual(Actor):
    def __init__(self, name):
        super().__init__(name)

        Window.bind(on_close=lambda inst: self.quit())
        self.run = True
        self.paused = False
        self.auto_end_turn_time = .8  # second
        self.view = View()
        self.view.ids.quit.bind(on_press=lambda inst: self.quit())
        self.view.ids.pause.bind(on_press=lambda inst: self.toggle_pause())
        self.view.ids.map.bind(on_touch_down=lambda inst, touch: self.move(touch.pos))

    def toggle_pause(self):
        self.paused = not self.paused

    def show_tile(self, tile, **distortions):
        super().show_tile(tile, **distortions)
        self.view.add_tile(tile)

    def show_troop(self, troop, **distortions):
        super().show_troop(troop, **distortions)
        self.view.add_troop(troop)

    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        if self.entity.troop:
            self.view.focus_center = self.entity.troop.pos
            self.view.center_camera()

        self.view.ids.current_turn.text = str(turn)
        self.run = True
        start = time()
        while self.run and (self.paused or time() - start < self.auto_end_turn_time):
            sleep(.05)

        self.end_turn()

    def path_to(self, x, y):
        super().path_to(x, y)
        if self.walk_path:
            if self.troop_target:
                self.view.move_target(int(x), int(y))
            else:
                self.view.set_target(int(x), int(y))
        else:
            self.view.unset_target()

    def move(self, pos):
        # absolute position in window
        ax, ay = pos
        # position on map widget
        mx, my = ax - self.view.ids.map.x, ay - self.view.ids.map.y
        # target position
        tx, ty = mx / assets.SIZE_MOD, my / assets.SIZE_MOD
        if not self.troop_target:
            troops = list(filter(
                lambda t: t.pos == (int(tx), int(ty)) and t.id != self.entity.troop.id,
                self.perception.troops.values()
            ))
            if troops:
                self.troop_target = troops[0]
        self.path_to(tx, ty)

    def quit(self):
        self.pre_processing.append(Quit(self))
        self.run = False
        self.paused = False
        App.get_running_app().stop()

    def move_troop(self, troop_id, x, y):
        super().move_troop(troop_id, x, y)
        self.view.move_troop(troop_id, x, y)

        if troop_id == self.entity.troop.id and not self.walk_path:
            self.view.unset_target()
            self.troop_target = None
