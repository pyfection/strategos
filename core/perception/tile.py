

from .mixins import CopyMixin


class Tile(CopyMixin):
    DEFAULT_FERTILITY = 0  # Number of people tile can sustain without modifiers
    type = 'tile'

    def __init__(self, perception, x, y, z=0, dominion=None, population=0, base_fertility=0):
        self._perception = perception
        self.x = x
        self.y = y
        self.z = z
        self.population = population
        self.base_fertility = base_fertility or self.DEFAULT_FERTILITY
        self._dominion = dominion

        perception.tiles[(x, y)] = self

    @property
    def pos(self):
        return self.x, self.y

    @property
    def fertility(self):
        return self.base_fertility

    @property
    def dominion(self):
        return self._perception.dominions.get(self._dominion)

    @dominion.setter
    def dominion(self, dominion):
        self._dominion = dominion.id

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


class Forest(Tile):
    DEFAULT_FERTILITY = 5
    type = 'forest'


class Hill(Tile):
    DEFAULT_FERTILITY = 5
    type = 'hill'


class Mountain(Tile):
    type = 'mountain'


class WoodBridge(Tile):
    type = 'wood_bridge'


class River(Tile):
    type = 'river'

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
