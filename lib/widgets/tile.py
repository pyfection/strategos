

from kivy.uix.image import Image


class Tile(Image):
    SIZE = 32

    def __init__(self, name, **kwargs):
        super().__init__(
            source=f'atlas://assets/tiles/{name}',
            size_hint=(None, None),
            size=kwargs.pop('size', (self.SIZE, self.SIZE)),
            color=[1, 1, 1, 1],
            **kwargs
        )
