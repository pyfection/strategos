

import random
from uuid import uuid4

from core.perception.troop import Troop


class Event:
    PRIO = 0


class Move(Event):
    PRIO = 3

    def __init__(self, troop_id, x, y):
        super().__init__()
        self.troop_id = troop_id
        self.x = x
        self.y = y

    def trigger(self, actor):
        actor.move_troop(self)


class Attack(Event):
    PRIO = 4
    STRENGTH_MOD = .1

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self.effectiveness_modifier = round(random.uniform(.5, 2), 2)
        self.reduce_amount = 0

    def trigger(self, actor):
        actor.attack_troop(self)


class Quit(Event):
    PRIO = 100

    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, actor):
        actor.quit_actor(self)


class SpawnTroop(Event):
    def __init__(self, id=None, name=None, leader=None, units=0, experience=.1, x=None, y=None):
        self.id = id or uuid4()
        self.name = name
        self.leader = leader
        self.units = units
        self.experience = experience
        self.x = x
        self.y = y
        self.troop = None

    def process(self, world):
        troop = Troop(
            id=self.id,
            name=self.name,
            leader=self.leader,
            units=self.units,
            experience=self.experience,
            x=self.x,
            y=self.y,
        )
        world.perception.troops[self.id] = troop
        self.troop = troop

        return True

    def trigger(self, actor):
        actor.show_troop(self.troop)

        return super().trigger(actor)


class Uncover(Event):
    PRIO = 2

    def __init__(self, x, y, requester):
        self.x, self.y = x, y
        self.requester = requester
        self.tile = None

    def trigger(self, actor):
        actor.uncover_tile(self)


class Discover(Event):
    PRIO = 1

    def __init__(self, troop_id=None, troop=None):
        self.troop_id = troop_id
        self.troop = troop

    def trigger(self, actor):
        actor.discover_troop(self)
