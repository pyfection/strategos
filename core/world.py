

import random
from threading import Thread
from uuid import uuid4
import logging

import logging_conf
from core.actor.ai import AI
from core.entity import Entity
from core.tile import TILE_TYPES
from core.troop import Troop
from core.faction import Faction
from helpers.loader import load_map, load_game, save_game
from helpers.convert import pos_to_coord, coord_to_pos


class World:
    def __init__(self, seed=None):
        self.seed = seed
        self.tiles = {}
        self.entities = {}
        self.troops = {}
        self.factions = {}
        self.actors = []
        self.current_turn = 0
        logging.info(f"Worldseed: {seed}")
        random.seed(seed)

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

            for p_troop_id, p_troop_dict in entity_dict.get('troops').items():
                p_troop = Troop(id=p_troop_id, **p_troop_dict)
                p_troop.leader = self.entities.get(p_troop.leader)
                entity.troops[p_troop_id] = p_troop

            for p_faction_id, p_faction_dict in game.get('factions').items():
                p_faction = Faction(id=p_faction_id, **p_faction_dict)
                p_faction.leader = self.entities.get(p_faction.leader)
                entity.factions[p_faction_id] = p_faction

        for tile_coord, tile_dict in game.get('tiles').items():
            x, y = coord_to_pos(tile_coord)
            owner = self.entities.get(tile_dict.get('owner'))
            Tile = TILE_TYPES[tile_dict.get('type', 'grass')]
            tile = Tile(x=x, y=y, z=tile_dict.get('z', 0), owner=owner)
            self.tiles[tile_coord] = tile

        for troop_id, troop_dict in game.get('troops').items():
            troop = Troop(id=troop_id, **troop_dict)
            troop.leader = self.entities.get(troop.leader)
            self.troops[troop_id] = troop

        for faction_id, faction_dict in game.get('factions').items():
            faction = Faction(id=faction_id, **faction_dict)
            faction.leader = self.entities.get(faction.leader)
            self.factions[faction_id] = faction

        return self

    @property
    def is_running(self):
        return any([a for a in self.actors if not isinstance(a, AI)])

    def save(self, game_name):
        game = {
            'seed': self.seed,
            'actor_entity_mapping': {
                actor.name: actor.entity.id for actor in self.actors
            },
            'entities': {},
            'tiles': {},
            'troops': {},
            'factions': {},
        }

        for id, entity in self.entities.items():
            entity_dict = {
                'name': entity.name,
                'ruler': entity.ruler_id,
                'troop': entity.troop_id,
                'entities': {},
                'tiles': {},
                'troops': {},
                'factions': {}
            }
            for p_id, p_entity in entity.entities.items():
                entity_dict['entities'][p_id] = {
                    'name': p_entity.name,
                    'ruler': p_entity.ruler_id,
                    'troop': p_entity.troop_id,
                    'entities': {},
                    'tiles': {},
                    'troops': {},
                    'factions': {}
                }
            for p_coord, p_tile in entity.tiles.items():
                entity_dict['tiles'][p_coord] = {
                    'z': p_tile.z,
                    'type': p_tile.type,
                    'owner': p_tile.owner.id if p_tile.owner else None
                }
            for p_id, p_troop in entity.troops.items():
                entity_dict['troops'][p_id] = {
                    'name': p_troop.name,
                    'elites': p_troop.elites,
                    'levies': p_troop.levies,
                    'x': p_troop.x,
                    'y': p_troop.y,
                }
            for p_id, p_faction in entity.factions.items():
                entity_dict['factions'][p_id] = {
                    'name': p_faction.name,
                    'leader': p_faction.leader.id if p_faction.leader else None
                }
            game['entities'][id] = entity_dict

        for coord, tile in self.tiles.items():
            game['tiles'][coord] = {
                'z': tile.z,
                'type': tile.type,
                'owner': tile.owner.id if tile.owner else None
            }

        for id, troop in self.troops.items():
            game['troops'][id] = {
                'name': troop.name,
                'elites': troop.elites,
                'levies': troop.levies,
                'x': troop.x,
                'y': troop.y,
            }
        for id, faction in self.factions.items():
            game['factions'][id] = {
                'name': faction.name,
                'leader': faction.leader.id if faction.leader else None
            }

        save_game(game, game_name)

    def get_ais(self):
        return [a for a in self.actors if isinstance(a, AI)]

    def add_actor(self, actor):
        ais = self.get_ais()
        for ai in ais:
            if ai.name == actor.name:
                self.actors.remove(ai)
                actor.entity = ai.entity
                break
        else:
            if ais:
                ai = random.choice(ais)
                self.actors.remove(ai)
                actor.entity = ai.entity
            else:
                entity = Entity()
                self.entities[entity.id] = entity
                actor.entity = entity.copy()
        if not actor.entity.troop:
            print(1, actor.entity, actor.entity.id)
            troop = Troop(elites=0, levies=0)
            self.troops[troop.id] = troop
            actor.entity.troop_id = troop.id
            print(2, actor.entity.troop_id)
            actor.entity.troops[troop.id] = troop.copy()
            print(3, actor.entity.troops)

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
            if actor.entity:
                entity = actor.entity.copy()
            else:
                entity = Entity()
            if entity.id not in self.entities:
                self.entities[entity.id] = entity
            settlement.owner = entity
            if not actor.entity:
                actor.set_entity(entity.copy())
            actor.reveal_tile(settlement.copy())
            if actor.entity.troop:
                actor.entity.troop.x = settlement.x
                actor.entity.troop.y = settlement.y

    def update(self):
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

    def run(self):
        logging.info("Started to run world")
        while self.is_running:
            self.update()
        logging.info("World is no longer running")

    def quit_actor(self, actor):
        self.actors.remove(actor)
        self.actors.append(AI(str(uuid4()), actor.entity))
