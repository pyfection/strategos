

from uuid import uuid4

from .mixins import CopyMixin


class Entity(CopyMixin):
    def __init__(self, perception, id=None, name=None, ruler_id=None, troop_id=None, faction_id=None):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self.ruler_id = ruler_id
        self.troop_id = troop_id
        self.faction_id = faction_id

        perception.entities[id] = self

    @property
    def perception(self):
        return self._perception

    @property
    def ruler(self):
        return self._perception.entities[self.ruler_id]

    @property
    def troop(self):
        return self._perception.troops[self.troop_id]

    @property
    def faction(self):
        return self._perception.factions[self.faction_id]
