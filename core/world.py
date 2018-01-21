

import random
from threading import Thread
from uuid import uuid4
import logging

import logging_conf
from core.actor.ai import AI
from core.entity import Entity
from core.troop import Troop
from core.perception import Perception
from helpers.loader import save_game


class World:
    def __init__(self, setup):
        self.seed = setup.get('seed')
        self.actors = setup.get('actors', [])
        self.current_turn = setup.get('current_turn', 0)
        self.perception = Perception.load(setup)
        logging.info(f"Worldseed: {self.seed}")
        random.seed(self.seed)

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

    def assign_entities_to_actors(self):
        entities = list(self.perception.entities.values())
        for actor in self.actors:
            try:
                entity = random.choice(entities)
            except IndexError:
                perception = Perception()
                entity = Entity(perception=perception)
                actor.entity_id = entity.id
                actor.perception = perception
                actor.show_entity(entity)
                self.perception.show_entity(entity)
            else:
                entities.remove(entity)
                actor.perception = entity.perception

    def distribute_settlements(self):
        homeless = [a for a in self.actors if a.entity]
        for coord, tile in self.perception.tiles.items():
            if tile.type != 'settlement':
                continue
            settlement = tile
            try:
                actor = homeless.pop(0)
            except IndexError:
                perception = Perception()
                entity = Entity(perception=perception)
                actor = AI(str(uuid4()), entity_id=entity.id)
                actor.perception = perception
                actor.show_entity(entity)
                self.perception.show_entity(entity)
                self.actors.append(actor)
            entity_id = actor.entity.id
            entity = self.perception.entities[entity_id]
            settlement.owner = entity
            actor.show_tile(settlement, owner=actor.entity)

    def assign_troops_to_actors(self):
        for actor in self.actors:
            if actor.entity.troop:
                continue
            visible_tiles = list(actor.perception.tiles.values())
            try:
                tile = random.choice(visible_tiles)
            except IndexError:
                raise IndexError(f"Actor {actor.name} has no visible tiles")
            troop = Troop(name=f"{actor.entity.name}'s Host", x=tile.x, y=tile.y)
            self.perception.troops[troop.id] = troop
            actor.show_troop(troop)
            actor.entity.troop = actor.perception.troops[troop.id]

    def reveal_all_tiles(self):
        for actor in self.actors:
            if not actor.entity:
                continue
            for tile in self.perception.tiles.values():
                actor.show_tile(tile)

    def reveal_all_troops(self):
        for actor in self.actors:
            if not actor.entity:
                continue
            for troop in self.perception.troops.values():
                actor.show_troop(troop)

    def update(self):
        threads = []

        # Collect events from actors and trigger them on the world
        actions = sorted([actor.action for actor in self.actors if actor.action], key=lambda k: k.PRIO)
        for actor in self.actors:
            actor.action = None
        for action in actions:
            action.trigger(self)

        # Tell actors to update
        for actor in self.actors:
            t = Thread(target=actor.do_turn, kwargs={'turn': self.current_turn, 'events': actions})
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
        replacement = AI(
            name=str(uuid4()),
            entity_id=actor.entity_id,
            perception=actor.perception,
            events=actor.events
        )
        self.actors.append(replacement)

    def move_troop(self, troop_id, x, y):
        troop = self.perception.troops[troop_id]
        troop.x = x
        troop.y = y
