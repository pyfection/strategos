

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
        self.view = View()
        self.view.ids.quit.bind(on_press=lambda inst: self.quit())
        self.view.ids.end_turn.bind(on_press=lambda inst: self.end_turn())
        self.view.ids.map.bind(on_touch_down=lambda inst, touch: self.move(touch.pos))

    def show_tile(self, tile, **distortions):
        super().show_tile(tile, **distortions)
        self.view.add_tile(tile)

    def show_troop(self, troop, **distortions):
        super().show_troop(troop, **distortions)
        self.view.add_troop(troop)

    def do_turn(self, turn, events):
        for event in events:
            event.trigger(self)
        if self.entity.troop:
            self.view.focus_center = self.entity.troop.x, self.entity.troop.y
            self.view.center_camera()
        self.view.ids.current_turn.text = str(turn)
        self.run = True
        while self.run:
            continue

    def move(self, pos):
        # absolute position in window
        ax, ay = pos
        # position on map widget
        mx, my = ax - self.view.ids.map.x, ay - self.view.ids.map.y
        # target position
        tx, ty = mx / assets.SIZE_MOD, my / assets.SIZE_MOD
        self.path_to(tx, ty)

    def end_turn(self):
        self.run = False
        super().end_turn()

    def quit(self):
        self.events.append(Quit(self))
        self.run = False
        App.get_running_app().stop()

    def move_troop(self, troop_id, x, y):
        super().move_troop(troop_id, x, y)
        self.view.move_troop(troop_id, x, y)
