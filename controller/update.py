

ACTOR = 'actors'
TILE = 'tiles'


class Update:
    __slots__ = ['causer', 'tiles', 'actors']
    def __init__(self, causer):
        self.causer = causer
        self.tiles = []
        self.actors = []

    def add(self, obj, identifiers, changes):
        update = {
            'identifiers': identifiers,
            'changes': changes,
        }
        obj = getattr(self, obj)
        obj.append(update)

    def update(self, update):
        self.tiles += update.tiles
        self.actors += update.actors
