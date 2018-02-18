

from .mixins import CopyMixin


class Dominion(CopyMixin):
    def __init__(self, perception, name, ruler, capital):
        self._perception = perception
        self.name = name
        self.ruler = ruler
        self.capital = capital
