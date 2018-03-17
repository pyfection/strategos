

from .mixins import CopyMixin


class Tile(CopyMixin):
    DEFAULT_FERTILITY = 0  # Number of people tile can sustain without modifiers
    BREED_MOD = .1
    type = 'tile'

    def __init__(self, perception, x, y, z=0, dominion_id=None, population=0, base_fertility=None):
        self._perception = perception
        self.x = x
        self.y = y
        self.z = z
        self.population = population
        self.base_fertility = self.DEFAULT_FERTILITY if base_fertility is None else base_fertility
        self.dominion_id = dominion_id

        perception.tiles[(x, y)] = self

    @property
    def pos(self):
        return self.x, self.y

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    @property
    def fertility(self):
        return self.base_fertility

    @property
    def breed_mod(self):
        remaining = max(self.fertility - self.population, 0)
        return self.BREED_MOD * remaining

    @property
    def dominion(self):
        return self._perception.dominions.get(self.dominion_id)

    @dominion.setter
    def dominion(self, dominion):
        self.dominion_id = dominion.id

    def to_dict(self):
        return {
            'pos': (self.x, self.y),
            'z': self.z,
            'population': self.population,
            'base_fertility': self.base_fertility,
            'dominion_id': self.dominion_id,
            'type': self.type
        }

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
