

from controller.base import Base
from controller.update import Update, ACTOR, TILE
from model.actor import Actor as ActorModel
from model.tile import Tile


class Actor(Base):
    MODEL = ActorModel

    def __init__(self, model=None, **kwargs):
        super().__init__(model=model, **kwargs)
        self.type = self.__class__.__name__.lower()

    @classmethod
    def all(cls):
        return [TYPES[model.type](model=model) for model in cls.MODEL.all()]

    @classmethod
    def find(cls, **kwargs):
        return [TYPES[model.type](model=model) for model in cls.MODEL.find(**kwargs)]

    def update(self, callback, update):
        for tile_update in update.tiles:
            tile = Tile.find(perceiver=self, **tile_update['identifiers'])
            if tile:
                tile = tile[0]
            else:  # most likely tile is not visible to actor
                continue
            for key, value in tile_update['changes'].items():
                setattr(tile, key, value)

        update = Update(self.name)
        self.act(update, callback)

    def act(self, update, callback):
        raise NotImplementedError("Actor is a base class")

    @property
    def owned_tiles(self):
        return [t for t in self._model.owned_tiles if t.perceiver and t.perceiver.id == self.id]


class AI(Actor):
    def act(self, update, callback):
        for i, tile in enumerate(self.owned_tiles, 1):
            update.add(
                obj=TILE,
                identifiers={'x': tile.x, 'y': tile.y},
                changes={'units': tile.units+1}
            )
            if self.unplaced_units == i:
                break
        update.add(
            obj=ACTOR,
            identifiers={'name': self.name},
            changes={'unplaced_units': 0}
        )
        callback(update)


TYPES = {
    'ai': AI,
}
