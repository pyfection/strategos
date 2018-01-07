

from uuid import uuid4


class Troop:
    def __init__(self, id=None, name=None, leader=None, elites=None, levies=None):
        self.id = id or str(uuid4())
        self.name = name
        self.leader = leader
        self.elites = elites  # number
        self.levies = levies  # number

    def __setattr__(self, key, value):
        if key == 'leader':
            if hasattr(self, 'leader') and self.leader:
                self.leader.troop = None
            if value:
                entity = value
                entity.troop = self
        super().__setattr__(key, value)
