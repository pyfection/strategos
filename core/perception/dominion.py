

from uuid import uuid4

from .mixins import CopyMixin


class Dominion(CopyMixin):
    def __init__(self, perception, id, name, ruler, capital):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self._ruler = ruler
        self._capital = capital

        perception.dominions[id] = self

    @property
    def ruler(self):
        return self._perception.entities[self._ruler]

    @property
    def capital(self):
        return self._perception.tiles[self._capital]

    @property
    def tiles(self):
        return filter(lambda t: t._dominion == self.id, self._perception.tiles.values())

    @property
    def population(self):
        return sum([t.population for t in self.tiles])
