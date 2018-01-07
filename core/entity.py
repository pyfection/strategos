

from uuid import uuid4


class Entity:
    def __init__(self, id=None, name=None, ruler_id=None, troop_id=None):
        self.id = id or str(uuid4())
        self.name = name
        self.entities = {}
        self.tiles = {}
        self.troops = {}
        self.factions = {}
        self.ruler_id = ruler_id
        self.troop_id = troop_id

    @property
    def ruler(self):
        return self.entities.get(self.ruler_id)

    @property
    def troop(self):
        return self.troops.get(self.troop_id)

    def __setattr__(self, key, value):
        if key == 'troop_id':
            if hasattr(self, 'troop_id') and self.troop_id:
                if self.troop:
                    self.troop.entities.remove(self)
        super().__setattr__(key, value)
        if key == 'troop_id' and self.troop and value:
            self.troop.entities.append(self)

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__()
        for key, value in d.items():
            setattr(inst, key, value)
        return inst
