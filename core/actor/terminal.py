

from core.actor.actor import Actor
from core.event import Quit, Move


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

    def move(self, x, y):
        try:
            troop_id = self.troop.id
        except AttributeError:
            print("Does not lead a troop")
        else:
            self.events.append(Move(troop_id, x, y))

    def quit(self):
        self.action = Quit(self)
        self.end_turn()

    def quit_actor(self, actor):
        print("Actor quit:", actor.name)

    def move_troop(self, troop_id, x, y):
        print("Moved troop", troop_id, "to", x, y)
