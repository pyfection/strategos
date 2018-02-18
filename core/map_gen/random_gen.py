

from random import Random

from core.perception.tile import TILE_TYPES


class RandomGen:
    def __init__(self, seed=None):
        self.seed = seed
        self.random = Random()
        self.random.seed(seed)

    def get_tile(self, x, y):
        Tile = self.random.choice(list(TILE_TYPES.values()))
        tile = Tile(x, y)

        return tile
