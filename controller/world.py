

from controller.base import Base
from controller.actor import Actor
from controller.tile import Tile
from model.world import World as WorldModel


class World(Base):
    MODEL = WorldModel

    def generate_terrain(self, width=50, height=50):
        for x in range(width):
            for y in range(height):
                Tile(x=x, y=y)

    def distribute_tiles(self):
        actors = Actor.all()
        undistributed = Tile.find(owner=None)
        for tile in undistributed:
            for actor in actors:
                tile.owner = actor
