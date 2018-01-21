

import random

from helpers.convert import pos_to_coord


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
    # ToDo: whole Attack system has to be planned, this class is deprecated
    def __init__(self, source_x, source_y, target_x, target_y):
        raise NotImplementedError
        super().__init__()
        self.source_x = source_x
        self.source_y = source_y
        self.target_x = target_x
        self.target_y = target_y
        self.attacker_die = random.randint(1, 6)
        self.defender_die = random.randint(1, 6)

    def trigger(self, actor):
        target = actor.tiles.get(pos_to_coord(self.target_x, self.target_y))
        source = actor.tiles.get(pos_to_coord(self.source_x, self.source_y))

        source.units -= self.amount

        if attacker > defender:
            dif = attacker - defender
            target.units = max(0, target.units - dif)
        elif defender > attacker:
            dif = defender - attacker
            self.amount = max(0, self.amount - dif)
        else:
            target.units -= 1
            self.amount -= 1

        super().trigger(actor)


class Quit(Event):
    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, actor):
        actor.quit_actor(self.actor)
