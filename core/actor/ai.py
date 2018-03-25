

from core.actor.actor import Actor
from core.reactor import PerceptionReact


class AIReact(PerceptionReact):
    def on_troop_update(self, event):
        if not self.actor.troop_target and event.id not in self.actor.perception.troops:
            self.actor.troop_target_id = event.id
        super().on_troop_update(event)


class AI(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reactor = AIReact(self)

    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        self.end_turn()
