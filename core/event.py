

import random
from uuid import uuid4

from core.perception.troop import Troop

class classproperty(property):
    def __get__(self, cls, owner):
        return max([d.importance for d in owner.dependencies], default=0)


class Event:
    dependencies = ()

    @classproperty
    def importance(cls):
        return


class Quit(Event):
    dependencies = ()

    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, actor):
        actor.quit_actor(self)


class PerceptionUpdate(Event):
    dependencies = ()

    def __init__(self, percept, id, updates, pos):
        self.percept = percept
        self.id = id
        self.updates = updates
        self.x, self.y = pos

    def trigger(self, actor):
        actor.update_perception(self)


class Move(Event):
    dependencies = (Event,)

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
    STRENGTH_MOD = .1
    dependencies = (Move,)

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id

    def trigger(self, actor):
        actor.attack_troop(self)
