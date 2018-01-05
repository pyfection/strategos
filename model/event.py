

import random

from model.base import Base, models, where


class Event(Base):
    __table__ = 'event'
    TYPES = {}

    def __init__(self, turn, triggered=False, causer_id=None, perceiver_id=None, **kwargs):
        assert isinstance(turn, int)
        assert isinstance(triggered, bool)
        assert isinstance(causer_id, int) or causer_id is None
        assert isinstance(perceiver_id, int) or perceiver_id is None
        self.turn = turn
        self.triggered = triggered
        self.causer_id = causer_id
        self.perceiver_id = perceiver_id
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        if key == 'causer':
            self.causer_id = value.id
        elif key == 'perceiver':
            self.perceiver_id = value.id
        else:
            super().__setattr__(key, value)

    @property
    def causer(self):
        Actor = models['actor']
        return Actor.get(where('id') == self.causer_id)

    @property
    def perceiver(self):
        Actor = models['actor']
        return Actor.get(where('id') == self.perceiver_id)


class Attack(Event):
    type = 'attack'

    def __init__(self, target_x, target_y, source_x, source_y, amount, **kwargs):
        assert isinstance(target_x, int)
        assert isinstance(target_y, int)
        assert isinstance(source_x, int)
        assert isinstance(source_y, int)
        assert isinstance(amount, int)
        self.target_x = target_x
        self.target_y = target_y
        self.source_x = source_x
        self.source_y = source_y
        self.amount = amount
        self.attacker_die = random.randint(1, 6)
        self.defender_die = random.randint(1, 6)
        super().__init__(**kwargs)


class DistributeUnits(Event):
    type = 'distribute_units'

    def __init__(self, x, y, amount, **kwargs):
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(amount, int)
        self.x = x
        self.y = y
        self.amount = amount
        self.type = 'distribute_units'
        super().__init__(**kwargs)


class Quit(Event):
    type = 'quit'


models[Event.__table__] = Event
Event.TYPES[Attack.type] = Attack
Event.TYPES[DistributeUnits.type] = DistributeUnits
Event.TYPES[Quit.type] = Quit
