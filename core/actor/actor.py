

from helpers.convert import pos_to_coord


class Actor:
    def __init__(self, name, entity_id=None, perception=None):
        self.name = name  # unique identifier / player/account name
        self.entity_id = entity_id
        self.perception = perception
        self.events = []

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

    def move_troop(self, troop_id, x, y):
        troop = self.entity.troop
        troop.x, troop.y = x, y

    def quit_actor(self, actor):
        pass
