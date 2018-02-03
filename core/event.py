

import random
from uuid import uuid4

from core.troop import Troop


class Event:
    PRIO = 0

    def trigger(self, actor):
        return True


class Move(Event):
    PRIO = 1

    def __init__(self, troop_id, x, y):
        super().__init__()
        self.troop_id = troop_id
        self.x = x
        self.y = y

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

    def trigger(self, actor):
        attacker = actor.perception.troops[self.attacker_id]
        defender = actor.perception.troops[self.defender_id]
        if defender.units == 0 or attacker.units == 0:
            return False

        base = attacker.units * self.STRENGTH_MOD
        unit_ratio = attacker.units / defender.units  # attacker to defender ratio
        exp_ratio = attacker.experience / defender.experience
        effect = self.effectiveness_modifier
        kills = round(max(base * unit_ratio * exp_ratio * effect, 1))
        actor.change_troop_unit_amount(self.defender_id, -min(kills, defender.units))

        return super().trigger(actor)


class Quit(Event):
    def __init__(self, actor):
        self.actor = actor  # actor to be quit

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

    def trigger(self, actor):
        troop = Troop(
            id=self.id,
            name=self.name,
            leader=self.leader,
            units=self.units,
            experience=self.experience,
            x=self.x,
            y=self.y,
        )
        actor.show_troop(troop)

        return super().trigger(actor)
