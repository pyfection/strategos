

from uuid import uuid4


class Troop:
    def __init__(self, id=None, companions=None, name=None, leader=None, elites=None, levies=None):
        self.id = id or uuid4()
        self.companions = companions
        self.name = name or str(self.id)
        self.leader = leader
        self.elites = elites  # number
        self.levies = levies  # number
