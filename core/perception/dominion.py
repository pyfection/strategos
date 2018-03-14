

from uuid import uuid4

from .mixins import CopyMixin


class Dominion(CopyMixin):
    def __init__(self, perception, id, name, ruler_id, capital_pos):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self.ruler_id = ruler_id
        self.capital_pos = capital_pos

        perception.dominions[id] = self

    @property
    def ruler(self):
        return self._perception.entities[self.ruler_id]

    @property
    def capital(self):
        return self._perception.tiles[self.capital_pos]

    @property
    def tiles(self):
        return filter(lambda t: t.dominion_id == self.id, self._perception.tiles.values())

    @property
    def population(self):
        return sum([t.population for t in self.tiles])
