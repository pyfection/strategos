

from threading import Thread
from uuid import uuid4
import logging

import logging_conf
from core.actor.ai import AI
from core.entity import Entity
from core.tile import TILE_TYPES
from helpers.loader import load_map, load_game
from helpers.convert import pos_to_coord, coord_to_pos


class World:
    def __init__(self, seed=None):
        self.seed = seed
        self.tiles = {}
        self.entities = {}
        self.actors = []
        self.current_turn = 0

    @classmethod
    def load_savegame(cls, game_name):
        game = load_game(game_name)
        self = cls(game['seed'])

        for actor_name, entity_id in game.get('actor_entity_mapping').items():
            entity = Entity(id=entity_id)
            self.entities[entity_id] = entity
            try:
                actor = next(a for a in self.actors if a.name == actor_name)
                actor.entity = entity
            except StopIteration:
                actor = AI(name=actor_name, entity=entity)
                self.actors.append(actor)

        for entity_id, entity_dict in game.get('entities').items():
            entity = self.entities.get(entity_id, Entity(id=entity_id))
            for p_entity_id, p_entity_dict in entity_dict.get('entities').items():
                p_entity = Entity(id=entity_id, **p_entity_dict)
                entity.entities[p_entity_id] = p_entity

            for p_tile_coord, p_tile_dict in entity_dict.get('tiles').items():
                x, y = coord_to_pos(p_tile_coord)
                owner = entity.entities.get(p_tile_dict.get('owner'))
                Tile = TILE_TYPES[p_tile_dict.get('type', 'grass')]
                p_tile = Tile(x=x, y=y, z=p_tile_dict.get('z', 0), owner=owner)
                entity.tiles[p_tile_coord] = p_tile

        for tile_coord, tile_dict in game.get('tiles').items():
            x, y = coord_to_pos(tile_coord)
            owner = self.entities.get(tile_dict.get('owner'))
            Tile = TILE_TYPES[tile_dict.get('type', 'grass')]
            tile = Tile(x=x, y=y, z=tile_dict.get('z', 0), owner=owner)
            self.tiles[tile_coord] = tile

        return self

    @property
    def is_running(self):
        return any([a for a in self.actors if not isinstance(a, AI)])

    def add_actor(self, actor):
        ais = [a for a in self.actors if isinstance(a, AI)]
        for ai in ais:
            if ai.name == actor.name:
                self.actors.remove(ai)
                actor.entity = ai.entity
                break
        self.actors.append(actor)

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
        logging.info("Started to run world")
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
        logging.info("World is no longer running")

    def quit_actor(self, actor):
        self.actors.remove(actor)
        self.actors.append(AI(str(uuid4()), actor.entity))
