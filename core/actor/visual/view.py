

import os

from kivy.lang.builder import Builder
from kivy.uix.widget import Widget


class View(Widget):
    def __init__(self):
        kv_path = os.path.join(os.path.dirname(__file__), 'view.kv')
        Builder.load_file(kv_path)
        super().__init__()
