

from kivy.app import App
from kivy.clock import Clock

from core.event import Quit
from core.actor.actor import Actor
from .view import View


class Visual(Actor):
    def __init__(self, name):
        super().__init__(name)

        self.run = True
        self.view = View()
        self.view.ids.quit.bind(on_press=lambda inst: self.quit())

    def show_tile(self, tile, **distortions):
        super().show_tile(tile, **distortions)
        self.view.add_tile(tile)

    def show_troop(self, troop, **distortions):
        super().show_troop(troop, **distortions)
        self.view.add_troop(troop)

    def do_turn(self, turn, events):
        if self.entity.troop:
            self.view.focus_center = self.entity.troop.x, self.entity.troop.y
            self.view.center_camera()
        self.view.ids.current_turn.text = str(turn)
        self.run = True
        while self.run:
            continue

    def quit(self):
        self.events.append(Quit(self))
        self.run = False
        App.get_running_app().stop()
