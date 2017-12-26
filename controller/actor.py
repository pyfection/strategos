

from controller.base import Base
from model.actor import Actor as ActorModel


class Actor(Base):
    MODEL = ActorModel

    def __init__(self, name):
        super().__init__()
        self.name = name
