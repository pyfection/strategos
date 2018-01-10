

from uuid import uuid4


class Troop:
    def __init__(self, id=None, name=None, elites=None, levies=None, x=None, y=None):
        self.id = id or str(uuid4())
        self.name = name
        self.elites = elites  # number
        self.levies = levies  # number
        self.x = x
        self.y = y

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.pop('entities')
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        return inst
