

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.lang import Builder

Builder.load_string("""
<MapMode>:
  bg_color: 0, 0, 0, 0
  canvas.before:
    Color:
      rgba: self.bg_color
    Rectangle:
      pos: self.pos
      size: self.size
""")


class Target(Image):
    SIZE = 32

    def __init__(self, **kwargs):
        super().__init__(
            source=f'atlas://assets/overlays/target',
            size_hint=(None, None),
            size=(self.SIZE, self.SIZE),
            color=[1, 1, 1, 1],
            **kwargs
        )


class MapMode(Label):
    SIZE = 32
    bg_color = ListProperty([0, 0, 0, 0])

    def __init__(self, mode_type, bg_color=None, **kwargs):
        self.mode_type = mode_type
        super().__init__(size_hint=(None, None), size=(self.SIZE, self.SIZE), **kwargs)
        if bg_color:
            self.bg_color = bg_color
