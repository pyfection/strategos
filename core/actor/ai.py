

import random

from core.actor.actor import Actor


class AI(Actor):
    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        if not self.troop_target:
            troop = self.entity.troop
            targets = list(filter(lambda t: t.id != troop.id and t.units, self.perception.troops.values()))
            if targets:
                self.troop_target = random.choice(targets)
        self.end_turn()
