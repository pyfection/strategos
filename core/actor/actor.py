

from helpers.convert import pos_to_coord


class Actor:
    def __init__(self, name, entity=None):
        self.name = name  # unique identifier / player/account name
        self.entity = entity
        self.events = []

    def set_entity(self, entity):
        self.entity = entity
        self.reveal_entity(entity)

    def reveal_entity(self, entity):
        self.entity.entities[entity.id] = entity

    def reveal_tile(self, tile):
        self.entity.tiles[pos_to_coord(tile.x, tile.y)] = tile

    def do_turn(self, turn, events):
        self.current_turn = turn
        for event in events:
            event.trigger(self)

    def quit_actor(self, actor):
        pass
