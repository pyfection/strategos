

class Tile:
    type = 'tile'
    color = '#ffffff'
    def __init__(self, x, y, z=0, owner=None):
        self.x = x
        self.y = y
        self.z = z
        self.owner = owner

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__(d.pop('x'), d.pop('y'))
        for key, value in d.items():
            setattr(inst, key, value)
        if self.owner:
            self.owner = kwargs.get('owner') or self.owner.copy()
        return inst


class Grass(Tile):
    type = 'grass'
    color = '#3b7c27'


class Settlement(Tile):
    type = 'settlement'
    color = '#740000'


TILE_TYPES = {
    Tile.type: Tile,
    Grass.type: Grass,
    Settlement.type: Settlement,
}