

import random
from threading import Thread
from uuid import uuid4
import logging

import logging_conf
from core.actor.ai import AI
from core.perception import Perception
from helpers.loader import save_game
from core.mixins import EventResponseMixin


class World(EventResponseMixin):
    def __init__(self, setup):
        self.seed = setup.get('seed')
        random.seed(self.seed)
        self.actors = setup.get('actors', [])
        self.current_turn = setup.get('current_turn', 0)
        self.perception = Perception.load(setup)
        for actor in self.actors:
            actor.perception = Perception.load(setup)
            actor.setup()
        logging.info(f"Worldseed: {self.seed}")

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
                    'units': p_troop.units,
                    'experience': p_troop.experience,
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
                'units': troop.units,
                'experience': troop.experience,
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

    def update(self):
        threads = []

        # Collect events from actors and trigger them on the world
        actions = sorted([event for actor in self.actors for event in actor.actions], key=lambda k: k.PRIO)

        for actor in self.actors:
            actor.actions.clear()
        for action in actions.copy():
            success = action.process(self)
            if not success:
                actions.remove(action)

        # Tell actors to update
        for actor in self.actors:
            events = actions.copy()
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
        replacement = AI(
            name=str(uuid4()),
            entity_id=actor.entity_id,
            perception=actor.perception,
            events=actor.events
        )
        self.actors.append(replacement)
