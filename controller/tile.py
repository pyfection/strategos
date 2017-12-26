

from controller.base import Base
from model.tile import Tile as TileModel


class Tile(Base):
    MODEL = TileModel

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
