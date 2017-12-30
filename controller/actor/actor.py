

from controller.base import Base
from controller.event import IncreaseUnits, Quit
from model.actor import Actor as ActorModel


class Actor(Base):
    MODEL = ActorModel
    TYPES = {}

    def __init__(self, model=None, **kwargs):
        super().__init__(model=model, **kwargs)
        self.type = self.__class__.__name__.lower()

    @classmethod
    def all(cls):
        return [cls.TYPES[model.type](model=model) for model in cls.MODEL.all()]

    @classmethod
    def find(cls, **kwargs):
        return [cls.TYPES[model.type](model=model) for model in cls.MODEL.find(**kwargs)]

    @property
    def owned_tiles(self):
        return [t for t in self._model.owned_tiles if t.perceiver and t.perceiver.id == self.id]

    def do_turn(self, turn):
        self.current_turn = turn

    def increase_units(self):
        for i, tile in enumerate(self.owned_tiles):
            if self.unplaced_units == i:
                break
            IncreaseUnits(
                x=tile.x, y=tile.y,
                amount=1,
                causer=self,
                turn=self.current_turn
            )

    def quit(self):
        Quit(causer=self, turn=self.current_turn)

    def on_increase_units(self, event):
        pass

    def on_quit(self, event):
        pass
