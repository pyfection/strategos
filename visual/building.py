

from kivy.uix.image import Image


class Settlement(Image):
    SIZE = 32

    def __init__(self, faction, size, **kwargs):
        size = 100  # ToDo: add more settlement sizes and then round the size
        super().__init__(
            source=f'atlas://assets/factions/{faction}/buildings/settlement-{size}',
            size_hint=(None, None),
            size=(self.SIZE, self.SIZE),
            color=[1, 1, 1, 1],
            **kwargs
        )
