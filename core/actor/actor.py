

from core.event import Move
from helpers.maths import distance, limit_distance


class Actor:
    def __init__(self, name, entity_id=None, perception=None, events=None):
        self.name = name  # unique identifier / player/account name
        self.entity_id = entity_id
        self.perception = perception
        self.events = events or []
        self.walk_path = []

    @property
    def entity(self):
        if self.perception:
            return self.perception.entities.get(self.entity_id)
        else:
            return None

    def show_entity(self, entity, **distortions):
        self.perception.show_entity(entity, **distortions)

    def show_tile(self, tile, **distortions):
        self.perception.show_tile(tile, **distortions)

    def show_troop(self, troop, **distortions):
        self.perception.show_troop(troop, **distortions)

    def do_turn(self, turn, events):
        self.current_turn = turn
        for event in events:
            event.trigger(self)

    def end_turn(self):
        if self.walk_path:
            troop = self.entity.troop
            rem = troop.speed
            while self.walk_path and rem > 0:
                x, y = self.walk_path[0]
                lx, ly = limit_distance((troop.x, troop.y), (x, y), rem)
                dist = distance((troop.x, troop.y), (lx, ly))
                rem -= round(dist, 3)
                if rem > 0:
                    self.walk_path.pop(0)
                self.events.append(Move(self.entity.troop.id, lx, ly))

    def path_to(self, x, y):
        self.walk_path.append((x, y))

    def move_troop(self, troop_id, x, y):
        troop = self.entity.troop
        troop.x, troop.y = x, y

    def quit_actor(self, actor):
        pass
