

import os

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen


class GameSetup(Screen):
    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'game_setup.kv')
        Builder.load_file(kv_path)
        super().__init__(name='game_setup')
