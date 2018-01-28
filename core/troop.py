

from uuid import uuid4


class Troop:
    def __init__(self, id=None, name=None, leader=None, units=0, experience=.1, x=None, y=None):
        self.id = id or str(uuid4())
        self.name = name
        self.leader = leader
        self.units = units
        self.experience = experience
        self.x = x
        self.y = y

    @property
    def pos(self):
        return (self.x, self.y)

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        return inst

    def update(self, troop, **kwargs):
        troop = troop.copy(**kwargs)
        d = troop.__dict__.copy()
        for key, value in d.items():
            setattr(self, key, value)
