

from uuid import uuid4


class Entity:
    def __init__(self, id=None, name=None, ruler=None, troop=None, perception=None):
        self.id = id or str(uuid4())
        self.name = name
        self.ruler = ruler
        self.troop = troop
        self.perception = perception

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        return inst
