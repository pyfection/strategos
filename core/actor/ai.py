

import random

from helpers import maths
from core.actor.actor import Actor


class AI(Actor):
    def on_troop_discover(self, event):
        super().on_troop_discover(event)
        if not self.troop_target:
            self.troop_target_id = event.id

    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        self.end_turn()
