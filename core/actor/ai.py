

import random

from helpers import maths
from core.actor.actor import Actor


class AI(Actor):
    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        if self.troop.units:
            troop = self.troop
            targets = sorted(
                filter(
                    lambda t: t.id != troop.id and t.units,
                    self.perception.troops.values()
                ),
                key=lambda t: maths.distance(troop.pos, t.pos)
            )
            if targets:
                self.troop_target = targets[0]
        self.end_turn()
