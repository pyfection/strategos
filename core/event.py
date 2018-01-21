

import random


class Event:
    PRIO = 0

    def trigger(self, actor):
        return


class Move(Event):
    PRIO = 1

    def __init__(self, troop_id, x, y):
        super().__init__()
        self.troop_id = troop_id
        self.x = x
        self.y = y

    def trigger(self, actor):
        actor.move_troop(self.troop_id, self.x, self.y)

        super().trigger(actor)


class Attack(Event):
    PRIO = 2
    STRENGTH_MOD = .1

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id
        self.effectiveness_modifier = random.randint(.5, 2)

    def trigger(self, actor):
        attacker = actor.perception.troops[self.attacker_id]
        defender = actor.perception.troops[self.defender_id]

        base = attacker.units * self.STRENGTH_MOD
        unit_ratio = attacker.units / defender.units  # attacker to defender ratio
        exp_ratio = attacker.experience / defender.experience
        effect = self.effectiveness_modifier
        kills = max(base * unit_ratio * exp_ratio * effect, 1)
        defender.units -= min(kills, defender.units)

        super().trigger(actor)


class Quit(Event):
    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, actor):
        actor.quit_actor(self.actor)
