

from threading import Thread

from model.base import db
from controller.base import Base
from controller.actor import Actor
from controller.tile import Tile
from model.world import World as WorldModel
from controller.update import Update


class World(Base):
    MODEL = WorldModel

    def __init__(self, game_name, **kwargs):
        db.load_game(game_name)
        super(World, self).__init__(**kwargs)
        self.updates = {}

    def generate_terrain(self, width=10, height=10):
        for x in range(width):
            for y in range(height):
                Tile(x=x, y=y)

    def distribute_tiles(self):
        actors = Actor.all()
        undistributed = Tile.find(owner=None, perceiver=None)
        while undistributed:
            for actor in actors:
                tile = undistributed.pop(0)
                tile.owner = actor
                tile.units = 1
                tile.copy(perceiver=actor)

    def validate_update(self, update):
        # ToDo: sort out or correct invalid changes
        self.apply_update(update)
        actors = Actor.all()
        for actor in actors:
            actor_updates = self.updates.get(actor.name, Update('world'))
            actor_updates.update(update)
            self.updates[actor.name] = actor_updates

    def apply_update(self, update):
        for tile_update in update.tiles:
            tile = Tile.find(perceiver=None, **tile_update['identifiers'])[0]
            for key, value in tile_update['changes'].items():
                setattr(tile, key, value)

    def do_turn(self):
        actors = Actor.all()
        for actor in actors:
            update = self.updates.get(actor.name, Update('world'))
            t = Thread(target=actor.update, kwargs={'callback': self.validate_update, 'update': update})
            t.start()
        self.current_turn += 1
