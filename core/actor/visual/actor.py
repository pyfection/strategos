

from kivy.app import App

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

    def do_turn(self, turn, events):
        self.view.ids.current_turn.text = str(turn)
        self.run = True
        while self.run:
            continue

    def quit(self):
        self.events.append(Quit(self))
        self.run = False
        App.get_running_app().stop()
