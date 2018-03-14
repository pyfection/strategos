

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

    @property
    def pos(self):
        return self.x, self.y

    def trigger(self, actor):
        actor.move_troop(self)


class Attack(Event):
    PRIO = 4
    STRENGTH_MOD = .1

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id

    def trigger(self, actor):
        actor.attack_troop(self)


class Quit(Event):
    PRIO = 100

    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, actor):
        actor.quit_actor(self)


class PerceptionUpdate(Event):
    PRIO = 1

    def __init__(self, percept, id, updates, pos):
        self.percept = percept
        self.id = id
        self.updates = updates
        self.x, self.y = pos

    def trigger(self, actor):
        actor.update_perception(self)
