

from uuid import uuid4


class Troop:
    def __init__(self, id=None, name=None, leader=None, elites=None, levies=None):
        self.id = id or str(uuid4())
        self.name = name
        self.leader = leader
        self.elites = elites  # number
        self.levies = levies  # number
