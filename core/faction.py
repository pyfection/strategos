

from uuid import uuid4


class Faction:
    def __init__(self, id=None, name=None, leader=None):
        self.id = id or str(uuid4())
        self.name = name
        self.leader = leader

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        return inst