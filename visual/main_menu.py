

import os

from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen


class MainMenu(Screen):
    MOVE_ANIM = 'in_out_cubic'
    REVEAL_TILE_ANIM = 'in_quart'
    FOW_ANIM = 'in_cubic'
    ANIM_DUR = .7
    SIZE_MOD = 32

    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'main_menu.kv')
        Builder.load_file(kv_path)
        super().__init__()
