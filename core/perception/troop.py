

from uuid import uuid4

from helpers import maths
from .mixins import CopyMixin


class Troop(CopyMixin):
    def __init__(
            self, perception,
            id=None, name=None, leader_id=None,
            units=0, experience=.1, vigor=0,
            x=None, y=None, view_range=5):
        self._perception = perception
        self.id = id or str(uuid4())
        self.name = name
        self.leader_id = leader_id
        self.units = units
        self.experience = experience
        self.vigor = vigor
        self.x = x
        self.y = y
        self.view_range = view_range

        perception.troops[id] = self

    @property
    def pos(self):
        return (self.x, self.y)

    @pos.setter
    def pos(self, value):
        self.x, self.y = value

    @property
    def leader(self):
        try:
            return self._perception.entities[self.leader_id]
        except KeyError:
            raise AttributeError("Troop does not have a leader")

    @property
    def max_vigor(self):
        return self.experience

    @property
    def vigor_ratio(self):
        return self.vigor / self.max_vigor

    def in_view_range(self, x, y):
        return maths.distance(self.pos, (x, y)) <= self.view_range

    def to_dict(self):
        return {
            'name': self.name,
            'units': self.units,
            'experience': self.experience,
            'vigor': self.vigor,
            'pos': (self.x, self.y),
            'view_range': self.view_range,
            'leader_id': self.leader_id
        }
