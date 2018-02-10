

import random

from helpers import maths
from core.actor.actor import Actor


class AI(Actor):
    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        self.end_turn()

    def show_troop(self, troop, **distortions):
        super().show_troop(troop, **distortions)

        if not self.troop_target:
            self.troop_target = troop
