

from controller.actor.actor import Actor


class AI(Actor):
    def do_turn(self, turn):
        super().do_turn(turn)
        self.distribute_units()


Actor.TYPES['ai'] = AI
