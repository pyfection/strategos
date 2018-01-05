

from core.actor.actor import Actor


class Terminal(Actor):
    def __init__(self, name):
        super().__init__(name)
        self.run = True

    def do_turn(self, turn, events):
        super().do_turn(turn, events)
        print('New turn', turn)
        self.run = True
        while self.run:
            continue
        print("Ended Turn")

    def end_turn(self):
        self.run = False

    def quit_actor(self, actor):
        print("Actor quit:", actor.name)
