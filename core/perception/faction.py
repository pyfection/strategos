

from uuid import uuid4

from .mixins import CopyMixin


class Faction(CopyMixin):
    def __init__(self, perception, id=None, name=None, leader=None, capital=None):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self._leader = leader
        self._capital = capital  # (x, y)

        perception.factions[id] = self

    @property
    def leader(self):
        return self._perception.entities[self._leader]

    @property
    def capital(self):
        return self._perception.tiles[self._capital]
