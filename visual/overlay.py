

from kivy.uix.image import Image
from kivy.uix.widget import Widget


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


class MapMode(Image):
    SIZE = 32

    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), size=(self.SIZE, self.SIZE), **kwargs)
