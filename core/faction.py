

from uuid import uuid4


class Faction:
    def __init__(self, id=None, name=None, leader=None):
        self.id = id or str(uuid4())
        self.name = name
        self.leader = leader
