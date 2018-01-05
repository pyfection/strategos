

from model.base import Base, models, where


class Actor(Base):
    __table__ = 'actor'
    TYPES = {}

    def __init__(self, name, current_turn=0, unplaced_units=0, **kwargs):
        assert isinstance(name, str)
        assert isinstance(current_turn, int)
        assert isinstance(unplaced_units, int)
        self.name = name
        self.current_turn = current_turn
        self.unplaced_units = unplaced_units
        super().__init__(**kwargs)

    @property
    def owned_tiles(self):
        Tile = models['tile']
        return Tile.get(where('owner_id') == self.id) or []

    @property
    def perceived_tiles(self):
        Tile = models['tile']
        return Tile.get(where('perceiver_id') == self.id) or []

    @property
    def caused_events(self):
        Event = models['event']
        return Event.get(where('causer_id') == self.id) or []

    @property
    def perceived_events(self):
        Event = models['event']
        return Event.get(where('perceiver_id') == self.id) or []


class AI(Actor):
    type = 'ai'


class Terminal(Actor):
    type = 'terminal'


class World(Actor):
    type = 'world'


models[Actor.__table__] = Actor
Actor.TYPES[AI.type] = AI
Actor.TYPES[Terminal.type] = Terminal
Actor.TYPES[World.type] = World
