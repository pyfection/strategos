

from controller.base import Base
from controller.tile import Tile
from model.event import Event as EventModel


class Event(Base):
    MODEL = EventModel
    TYPES = {}

    def __init__(self, model=None, turn=None, causer=None, perceiver=None, validate=True, **kwargs):
        if model:
            super().__init__(model=model)
        else:
            # print(turn, causer)
            # print(turn is not None, bool(causer))
            assert turn is not None and causer
            super().__init__(
                type=kwargs.pop('type', None) or self.__class__.__name__.lower(),
                turn=turn,
                causer=causer,
                perceiver=perceiver or causer,
                **kwargs
            )
        if validate:
            self.validate()

    @classmethod
    def all(cls):
        return [cls.TYPES[model.type](model=model) for model in cls.MODEL.all()]

    @classmethod
    def find(cls, **kwargs):
        return [cls.TYPES[model.type](model=model) for model in cls.MODEL.find(**kwargs)]

    def validate(self):
        raise NotImplementedError("Event is a base class and has no validation")

    def trigger(self):
        assert not self.triggered
        self.triggered = True

    def copy(self, **kwargs):
        d = {
            'triggered': False,
            'validate': False
        }
        d.update(kwargs)
        return super().copy(**d)


class Attack(Event):
    def __init__(self, model=None, x=None, y=None, **kwargs):
        if model:
            super().__init__(model=model)
        else:
            assert x is not None and y is not None
            super().__init__(
                x=x,
                y=y,
                **kwargs
            )

    def validate(self):
        tile = Tile.find(x=self.x, y=self.y, perceiver=self.causer)[0]
        assert self.causer != tile.owner

    # def copy(self, **kwargs):
    #     params = {
    #         'x': self.x,
    #         'y': self.y,
    #         'causer': self.causer,
    #         'perceiver':self.perceiver,
    #         'validate': False
    #     }
    #     params.update(kwargs)
    #     return Attack(**params)


class DistributeUnits(Event):
    def __init__(self, model=None, x=None, y=None, amount=None, **kwargs):
        if model:
            super().__init__(model=model)
        else:
            assert x is not None and y is not None and amount is not None
            super().__init__(
                x=x,
                y=y,
                amount=amount,
                **kwargs
            )

    def validate(self):
        events = Event.find(causer=self.causer, turn=self.turn)
        total_amount = sum([e.amount for e in events if isinstance(e, DistributeUnits)])
        assert total_amount <= self.causer.unplaced_units
        tile = Tile.find(x=self.x, y=self.y, perceiver=self.causer)[0]
        assert tile.owner == self.causer

    def trigger(self):
        if self.causer == self.perceiver:
            self.causer.unplaced_units -= 1
        tile = Tile.find(x=self.x, y=self.y, perceiver=self.perceiver)[0]
        tile.units += self.amount
        super().trigger()
        self.perceiver.on_distribute_units(self)

    # def copy(self, **kwargs):
    #     params = {
    #         'x': self.x,
    #         'y': self.y,
    #         'amount': self.amount,
    #         'causer': self.causer,
    #         'perceiver':self.perceiver,
    #         'validate': False
    #     }
    #     params.update(kwargs)
    #     return Attack(**params)


class Quit(Event):
    def validate(self):
        assert self.causer.type != 'ai'  # AI can't quit

    def trigger(self):
        if self.causer == self.perceiver:
            self.causer.type = 'ai'
        super().trigger()
        self.perceiver.on_quit(self)


Event.TYPES['attack'] = Attack
Event.TYPES['distributeunits'] = DistributeUnits
Event.TYPES['quit'] = Quit