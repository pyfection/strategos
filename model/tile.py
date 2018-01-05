

from uuid import UUID

from model.base import Base, models, where


class Tile(Base):
    __table__ = 'tile'
    TYPES = {}

    def __init__(self, x, y, units=0, owner_id=None, perceiver_id=None, **kwargs):
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(units, int)
        assert owner_id is None or isinstance(owner_id, str)
        assert perceiver_id is None or isinstance(perceiver_id, str)
        self.x = x
        self.y = y
        self.units = units
        self.owner_id = owner_id
        self.perceiver_id = perceiver_id
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        if key == 'owner':
            self.owner_id = value.id
        elif key == 'perceiver':
            self.perceiver_id = value.id
        else:
            super().__setattr__(key, value)

    @property
    def owner(self):
        Actor = models['actor']
        return Actor.get(where('id') == self.owner_id)

    @property
    def perceiver(self):
        Actor = models['actor']
        return Actor.get(where('id') == self.perceiver_id)


class Grass(Tile):
    type = 'grass'


models[Tile.__table__] = Tile
Tile.TYPES[Grass.type] = Grass
