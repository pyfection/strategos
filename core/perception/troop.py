

from uuid import uuid4

from helpers import maths
from .mixins import CopyMixin


class Troop(CopyMixin):
    def __init__(
            self, perception, id=None, name=None, leader=None, units=0, experience=.1, x=None, y=None, view_range=5):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self.units = units
        self.experience = experience
        self.x = x
        self.y = y
        self.view_range = view_range
        self._leader = leader

        perception.troops[id] = self

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def leader(self):
        return self._perception.entities[self._leader]

    def in_view_range(self, x, y):
        return maths.distance(self.pos, (x, y)) <= self.view_range
