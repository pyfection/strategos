

from uuid import uuid4

from .mixins import CopyMixin


class Faction(CopyMixin):
    def __init__(self, perception, id=None, name=None, leader_id=None, capital_pos=None, color=None):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self.color = color or [1, 1, 1]
        self.leader_id = leader_id
        self.capital_pos = capital_pos  # (x, y)

        perception.factions[id] = self

    @property
    def leader(self):
        return self._perception.entities[self.leader_id]

    @property
    def capital(self):
        return self._perception.tiles[self.capital_pos]
