

import os

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button


class GameSetup(Screen):
    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'game_setup.kv')
        Builder.load_file(kv_path)
        super().__init__(name='game_setup')
        self.players = {}

        self.add_player('test_player')

    def add_player(self, name):
        self.players[name] = {}
        name = Label(text=name)
        options = Button(text="Options")
        self.ids.players.add_widget(name)
        self.ids.players.add_widget(options)
