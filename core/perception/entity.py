

from uuid import uuid4

from .mixins import CopyMixin


class Entity(CopyMixin):
    def __init__(self, perception, id=None, name=None, ruler=None, troop=None, faction=None):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self._ruler = ruler
        self._troop = troop
        self._faction = faction

        perception.entities[id] = self

    @property
    def perception(self):
        return self._perception

    @property
    def ruler(self):
        return self._perception.entities[self._ruler]

    @property
    def troop(self):
        return self._perception.troops[self._troop]

    @property
    def faction(self):
        return self._perception.factions[self._faction]
