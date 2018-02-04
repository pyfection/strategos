

import random
from uuid import uuid4

from core.troop import Troop


class Event:
    PRIO = 0

    def process(self, world):
        return True

    def trigger(self, actor):
        return True


class Move(Event):
    PRIO = 1

    def __init__(self, troop_id, x, y):
        super().__init__()
        self.troop_id = troop_id
        self.x = x
        self.y = y

    def process(self, world):
        return self.trigger(world)

    def trigger(self, actor):
        if (self.x, self.y) in [troop.pos for troop in actor.perception.troops.values() if troop.units]:
            return False
        actor.move_troop(self.troop_id, self.x, self.y)

        return super().trigger(actor)


class Attack(Event):
    PRIO = 3
    STRENGTH_MOD = .1

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self.effectiveness_modifier = round(random.uniform(.5, 2), 2)
        self.reduce_amount = 0

    def process(self, world):
        attacker = world.perception.troops[self.attacker_id]
        defender = world.perception.troops[self.defender_id]
        if defender.units == 0 or attacker.units == 0:
            return False

        base = attacker.units * self.STRENGTH_MOD
        unit_ratio = attacker.units / defender.units  # attacker to defender ratio
        exp_ratio = attacker.experience / defender.experience
        effect = self.effectiveness_modifier
        kills = round(max(base * unit_ratio * exp_ratio * effect, 1))
        self.reduce_amount = -min(kills, defender.units)

        return self.trigger(world)

    def trigger(self, actor):
        actor.change_troop_unit_amount(self.defender_id, self.reduce_amount)

        return super().trigger(actor)


class Quit(Event):
    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def process(self, world):
        return self.trigger(world)

    def trigger(self, actor):
        actor.quit_actor(self.actor)

        return super().trigger(actor)


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
    def __init__(self, x, y, requester):
        self.x, self.y = x, y
        self.requester = requester
        self.tile = None
        self.troop = None

    def process(self, world):
        self.tile = world.get_tile(self.x, self.y)
        self.troop = world.get_troop(self.x, self.y)
        return True

    def trigger(self, actor):
        if actor.name is not self.requester.name:
            return False

        actor.show_tile(self.tile)
        if self.troop:
            actor.show_troop(self.troop)

        return super().trigger(actor)


class Discover(Event):
    def __init__(self, troop_id):
        self.troop_id = troop_id
        self.troop = None

    def process(self, world):
        self.troop = world.perception.troops[self.troop_id]
        return True

    def trigger(self, actor):
        actor.show_troop(self.troop)

        return super().trigger(actor)
