

from controller.base import Base
from model.actor import Actor as ActorModel


class Actor(Base):
    MODEL = ActorModel

    def do_turn(self):
        raise NotImplementedError("Actor is a base class")


class AI(Actor):
    def do_turn(self):
        pass
