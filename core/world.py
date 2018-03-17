

import logging
import random
from threading import Thread
from uuid import uuid4

from core.actor.ai import AI
from core.mixins import EventResponseMixin
from core.event import Quit, PerceptionUpdate
from core.perception import Perception
from core.managers.dominion_manager import DominionManager
from helpers.loader import save_game
from helpers import maths


class WorldEventResponseMixin(EventResponseMixin):
    def _add_event_to_actor(self, event, actor):
        self.events.setdefault(actor.name, []).append(event)

    def _discover_tiles(self, actor):
        troop = self.perception.troops[actor.troop.id]
        origin = troop.pos

        tiles = []
        for i in range(-troop.view_range, troop.view_range + 1):
            for j in range(-troop.view_range, troop.view_range + 1):
                x = origin[0] + i
                y = origin[1] + j
                distance = maths.distance(origin, (x, y))
                if distance > troop.view_range:
                    continue
                if (x, y) not in actor.perception.tiles:
                    tile = self.perception.get_tile(x, y)
                    tiles.append(tile)

        return tiles

    def quit_actor(self, event):
        actor = event.actor
        self.actors.remove(actor)
        replacement = AI(
            name=str(uuid4()),
            perception=actor.perception,
            events=actor.events
        )
        self.actors.append(replacement)
        event = Quit(actor)
        for actor in self.actors:
            self._add_event_to_actor(event, actor)

    def move_troop(self, event):
        """What happens when an actor asked to move a troop"""
        occupied_positions = (troop.pos for troop in self.perception.troops.values() if troop.units)
        is_pos_occupied_by_other_troop = event.pos in occupied_positions
        if not is_pos_occupied_by_other_troop:
            troop = self.perception.troops[event.troop_id]
            if not troop.units:
                return
            troop.x, troop.y = event.x, event.y
            for actor in self.actors:
                if actor.troop:
                    actor_troop = actor.troop
                    if actor_troop.in_view_range(event.x, event.y):
                        if event.troop_id in actor.perception.troops:
                            move = PerceptionUpdate(
                                percept='troops',
                                id=event.troop_id,
                                updates={'pos': troop.pos},
                                pos=troop.pos
                            )
                            self._add_event_to_actor(move, actor)
                        else:
                            discover = PerceptionUpdate(
                                percept='troops',
                                id=event.troop_id,
                                updates=troop.to_dict(),
                                pos=troop.pos
                            )
                            self._add_event_to_actor(discover, actor)

                    if actor_troop.id == event.troop_id:
                        tiles = self._discover_tiles(actor)
                        for tile in tiles:
                            discover = PerceptionUpdate(
                                percept='tiles',
                                id=tile.pos,
                                updates=tile.to_dict(),
                                pos=tile.pos
                            )
                            self._add_event_to_actor(discover, actor)
                        for other_troop in self.perception.troops.values():
                            if other_troop.id == actor_troop.id or other_troop.id in actor.perception.troops:
                                continue
                            elif not other_troop.in_view_range(event.x, event.y):
                                continue
                            discover = PerceptionUpdate(
                                percept='troops',
                                id=other_troop.id,
                                updates=other_troop.to_dict(),
                                pos=other_troop.pos
                            )
                            self._add_event_to_actor(discover, actor)

    def attack_troop(self, event):
        attacker = self.perception.troops[event.attacker_id]
        defender = self.perception.troops[event.defender_id]
        if defender.units == 0 or attacker.units == 0:
            return

        base = attacker.units * event.STRENGTH_MOD
        unit_ratio = attacker.units / defender.units  # attacker to defender ratio
        exp_ratio = attacker.experience / defender.experience
        effectiveness_modifier = round(random.uniform(.5, 2), 2)
        kills = round(max(base * unit_ratio * exp_ratio * effectiveness_modifier, 1))
        amount = defender.units - min(kills, defender.units)
        defender.units += amount

        update = PerceptionUpdate(
            percept='troops',
            id=defender.id,
            updates={'units': amount},
            pos=defender.pos
        )

        for actor in self.actors:
            if actor.troop and actor.troop.in_view_range(defender.x, defender.y):
                self._add_event_to_actor(update, actor)


class World(WorldEventResponseMixin):
    def __init__(self, setup):
        self.seed = setup.get('seed')
        random.seed(self.seed)
        self.actors = setup.get('actors', [])
        self.current_turn = setup.get('current_turn', 0)
        self.perception = Perception.load(setup)
        self.perceptions = {
            id: Perception.load(perception, id)
            for id, perception in setup.get('perceptions', {}).items()
        }
        self.events = {}
        self.dominion_manager = DominionManager(self.perception)

        for actor in self.actors:
            entity_id = setup['actor_to_entity_mapping'][actor.name]
            actor.perception = self.perceptions[entity_id]
            tiles = self._discover_tiles(actor)
            for tile in tiles:
                actor.perception.tiles[tile.pos] = tile
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
            for p_pos, p_tile in entity.tiles.items():
                entity_dict['tiles'][p_pos] = {
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

        for pos, tile in self.tiles.items():
            game['tiles'][pos] = {
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

    def get_troop(self, x, y):
        for troop in self.perception.troops.values():
            if troop.pos == (x, y):
                return troop

    def update(self):
        threads = []

        actions = [event for actor in self.actors for event in actor.actions]
        actions += self.dominion_manager.actions
        actions = sorted(actions, key=lambda k: k.importance)

        self.dominion_manager.actions.clear()
        for actor in self.actors:
            actor.actions.clear()

        for action in actions.copy():
            action.trigger(self)

        self.dominion_manager.do_turn()

        # Tell actors to update
        for actor in self.actors:
            events = sorted(self.events.get(actor.name, []), key=lambda k: k.importance)
            t = Thread(target=actor.do_turn, kwargs={'turn': self.current_turn, 'events': events})
            threads.append(t)
            t.start()
        self.events.clear()

        # Wait for all actors to finish
        for thread in threads:
            thread.join()

        self.current_turn += 1

    def run(self):
        logging.info("Started to run world")
        while self.is_running:
            self.update()
        logging.info("World is no longer running")
