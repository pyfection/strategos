

from time import time, sleep
from math import floor

from kivy.app import App
from kivy.core.window import Window

from core.event import Quit, SpawnTroop
from core.actor.actor import Actor
from .view import View
from . import assets


class Visual(Actor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_close=lambda inst: self.quit())
        self.run = True
        self.paused = False
        self.auto_end_turn_time = .8  # second
        self.view = View(self)
        self.view.ids.quit.bind(on_press=lambda inst: self.quit())
        self.view.ids.pause.bind(on_press=lambda inst: self.toggle_pause())
        self.view.ids.map.bind(on_touch_down=lambda inst, touch: self.move(touch.pos))

    def setup(self):
        super().setup()
        for tile in self.perception.tiles.values():
            self.view.add_tile(tile)
        for troop in self.perception.troops.values():
            if troop.leader and troop.leader.faction:
                faction = troop.leader.faction.name
            else:
                faction = None
            self.view.add_troop(faction, troop)
            if self.troop and troop.id == self.troop.id:
                self.view.focus_center = self.troop.pos
                self.view.focus_radius = self.troop.view_range

    def toggle_pause(self):
        self.paused = not self.paused

    def spawn_troop(self, name, x=0, y=0, units=0, experience=0):
        event = SpawnTroop(
            name=name,
            units=int(units),
            experience=float(experience),
            x=int(x),
            y=int(y)
        )
        self.actions.append(event)

    def show_tile(self, tile, **distortions):
        super().show_tile(tile, **distortions)
        self.view.add_tile(tile)

    def show_troop(self, troop, **distortions):
        super().show_troop(troop, **distortions)
        if troop.units:
            if troop.leader and troop.leader.faction:
                faction = troop.leader.faction.name
            else:
                faction = None
            self.view.add_troop(faction, troop)

    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        self.view.ids.current_turn.text = str(turn)
        self.run = True
        start = time()
        while self.run and (self.paused or time() - start < self.auto_end_turn_time):
            sleep(.05)

        self.end_turn()

    def move(self, pos):
        if not self.troop.units:
            return
        # absolute position in window
        ax, ay = pos
        # position on map widget
        mx, my = ax - self.view.ids.map.x, ay - self.view.ids.map.y
        # target position
        tx, ty = floor(mx / assets.SIZE_MOD), floor(my / assets.SIZE_MOD)

        if (tx, ty) == self.troop.pos:
            return

        super().stop_actions()
        troops = list(filter(
            lambda t: t.pos == (tx, ty) and t.id != self.troop.id and t.units,
            self.perception.troops.values()
        ))
        if troops:
            self.troop_target = troops[0]
        self.view.set_target(tx, ty)
        self.path_to(tx, ty)

    def quit(self):
        self.actions.append(Quit(self))
        self.run = False
        self.paused = False
        App.get_running_app().stop()

    def move_troop(self, event):
        super().move_troop(event)
        self.view.move_troop(event.troop_id, event.x, event.y)
        if self.troop_target and self.troop_target.id == event.troop_id:
            self.view.move_target(event.x, event.y)

        if self.troop and event.troop_id == self.troop.id:
            self.view.focus_center = self.troop.pos
            self.view.center_camera()
            if not self.walk_path and not self.troop_target:
                self.view.unset_target()

    def stop_actions(self):
        self.view.unset_target()
        super().stop_actions()

    def change_troop_unit_amount(self, troop_id, amount):
        super().change_troop_unit_amount(troop_id, amount)
        troop = self.perception.troops[troop_id]

        self.view.change_troop_unit_amount(troop_id, amount)
        if not troop.units:
            self.view.remove_troop(troop_id)