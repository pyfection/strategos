

from kivy.uix.image import Image


class Troop(Image):
    SIZE = 32

    def __init__(self, faction, **kwargs):
        super().__init__(
            source=f'atlas://assets/factions/{faction}/troops/troop',
            size_hint=(None, None),
            size=(self.SIZE, self.SIZE),
            color=[1, 1, 1, 1],
            **kwargs
        )
