

from uuid import uuid4


class Entity:
    def __init__(self, id=None, name=None, ruler=None):
        self.id = id or uuid4()
        self.name = name or str(self.id)
        self.ruler = ruler
        self.entities = {}
        self.tiles = {}

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        if self.ruler:
            self.owner = kwargs.get('ruler') or self.ruler.copy()
        return inst
