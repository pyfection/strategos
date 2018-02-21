

from .mixins import CopyMixin
from helpers.convert import pos_to_coord


class Tile(CopyMixin):
    DEFAULT_FERTILITY = 0
    type = 'tile'
    color = '#ffffff'

    def __init__(self, perception, x, y, z=0, dominion=None, population=0, base_fertility=0):
        self._perception = perception
        self.x = x
        self.y = y
        self.z = z
        self.population = population
        self.base_fertility = base_fertility or self.DEFAULT_FERTILITY
        self._dominion = dominion

        perception.tiles[pos_to_coord(x, y)] = self

    @property
    def pos(self):
        return self.x, self.y

    @property
    def fertility(self):
        return self.base_fertility

    @property
    def dominion(self):
        return self._perception.dominions[self._dominion]

    def copy(self, **kwargs):
        d = self.__dict__.copy()
        d.update(kwargs)
        inst = self.__class__(d.pop('x'), d.pop('y'))
        for key, value in d.items():
            setattr(inst, key, value)
        if inst.owner:
            inst.owner = kwargs.get('owner') or self.owner.copy()
        return inst

    def passable(self, by):
        """
        check if tile is passable by "by"
        :param by: troop or any other similar object
        :return: bool
        """
        return True


class Grass(Tile):
    DEFAULT_FERTILITY = 10
    type = 'grass'
    color = '#3b7c27'


class Forest(Tile):
    DEFAULT_FERTILITY = 5
    type = 'forest'
    color = '#1c3c16'


class Hill(Tile):
    DEFAULT_FERTILITY = 5
    type = 'hill'
    color = '#928f34'


class Mountain(Tile):
    type = 'mountain'
    color = '#586069'


class WoodBridge(Tile):
    type = 'wood_bridge'
    color = '#966a44'


class River(Tile):
    type = 'river'
    color = '#1886ab'

    def passable(self, by):
        return False


TILE_TYPES = {
    Grass.type: Grass,
    Forest.type: Forest,
    Hill.type: Hill,
    Mountain.type: Mountain,
    WoodBridge.type: WoodBridge,
    River.type: River,
}
