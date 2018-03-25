

from time import time, sleep
from math import floor

from kivy.app import App
from kivy.core.window import Window

from core.event import Quit
from core.actor.actor import Actor
from core.reactor import PerceptionReact
from .view import View
from . import assets


class VisualReact(PerceptionReact):
    def on_troop_update(self, event):
        super().on_troop_update(event)
        troop = self.actor.perception.troops[event.id]
        if event.id not in self.actor.view.troops:
            try:
                faction = troop.leader.faction
            except AttributeError:
                faction = None
            self.actor.view.add_troop(faction, troop)

    def on_troop_pos(self, id, pos):
        super().on_troop_pos(id, pos)
        self.actor.view.move_troop(id, *pos)
        if self.actor.troop_target and self.actor.troop_target.id == id:
            self.actor.view.move_target(*pos)

        if self.actor.troop and id == self.actor.troop.id:
            self.actor.view.focus_center = self.actor.troop.pos
            self.actor.view.center_camera()
            if not self.actor.walk_path and not self.actor.troop_target:
                self.actor.view.unset_target()

    def on_troop_units(self, id, units):
        troop = self.actor.perception.troops[id]
        dif = units - troop.units
        was_dead = troop.units == 0

        super().on_troop_units(id, units)

        if was_dead and units > 0:
            return

        self.actor.view.change_troop_unit_amount(id, dif)
        if not troop.units:
            self.actor.view.remove_troop(id)

    def on_tile_update(self, event):
        super().on_tile_update(event)
        if event.pos not in self.actor.view.tiles:
            tile = self.actor.perception.tiles[event.pos]
            self.actor.view.add_tile(tile)


class Visual(Actor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reactor = VisualReact(self)

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

    def stop_actions(self):
        self.view.unset_target()
        super().stop_actions()
