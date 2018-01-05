

from threading import Thread
from uuid import uuid4

from core.actor.ai import AI
from core.entity import Entity
from helpers.loader import load_map
from helpers.convert import pos_to_coord


class World:
    def __init__(self):
        self.tiles = {}
        self.entities = {}
        self.actors = []
        self.current_turn = 0

    @classmethod
    def load_savegame(cls, game_name):
        raise NotImplementedError("This feature is not supported yet")

    @property
    def is_running(self):
        return any([a for a in self.actors if not isinstance(a, AI)])

    def load_map(self, map_name):
        tiles = load_map(map_name)
        for tile in tiles:
            self.tiles[pos_to_coord(tile.x, tile.y)] = tile

    def distribute_settlements(self):
        homeless = list(self.actors)
        for coord, tile in self.tiles.items():
            if tile.type != 'settlement':
                continue
            settlement = tile
            try:
                actor = homeless.pop(0)
            except IndexError:
                actor = AI(str(uuid4()))
                self.actors.append(actor)
            entity = Entity()
            self.entities[entity.id] = entity
            settlement.owner = entity
            actor.set_entity(entity.copy())
            actor.reveal_tile(tile.copy())

    def run(self):
        while self.is_running:
            threads = []

            # Collect events from actors and trigger them on the world
            events = [event for actor in self.actors for event in actor.events]
            for event in events:
                event.trigger(self)

            # Tell actors to update
            for actor in self.actors:
                t = Thread(target=actor.do_turn, kwargs={'turn': self.current_turn, 'events': events})
                threads.append(t)
                t.start()

            # Wait for all actors to finish
            for thread in threads:
                thread.join()

            self.current_turn += 1

    def quit_actor(self, actor):
        self.actors.remove(actor)
        self.actors.append(AI(str(uuid4()), actor.entity))
