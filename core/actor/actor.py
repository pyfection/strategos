

import math

from helpers import maths
from helpers.convert import pos_to_coord, coord_to_pos
from core.event import Move, Attack, Uncover, Discover
from core.mixins import EventDistortedResponseMixin


class Actor(EventDistortedResponseMixin):
    def __init__(self, name, perception=None, events=None):
        self.name = name  # unique identifier / player/account name
        self.perception = perception
        self.events = events or []  # events coming from outside
        self.actions = []  # actions (events) actor wants to do
        self.walk_path = []
        self.troop_target = None  # troop target

    def _discover(self, origin=None):
        if not self.troop:
            return
        if not origin:
            origin = self.troop.pos
        for i in range(-self.troop.view_range, self.troop.view_range+1):
            for j in range(-self.troop.view_range, self.troop.view_range+1):
                x = origin[0] + i
                y = origin[1] + j
                distance = maths.distance(origin, (x, y))
                if distance > self.troop.view_range:
                    continue
                coord = pos_to_coord(x, y)
                if coord not in self.perception.tiles:
                    action = Uncover(x, y, self)
                    self.actions.append(action)

    def setup(self):
        self._discover()

    @property
    def entity(self):
        if self.perception:
            return self.perception.entity

    @property
    def troop(self):
        entity = self.entity
        if entity:
            return entity.troop

    def assign_troop(self, troop):
        self.show_troop(troop)
        self.entity.troop = self.perception.troops[troop.id]

    def show_entity(self, entity, **distortions):
        self.perception.show_entity(entity, **distortions)

    def show_tile(self, tile, **distortions):
        self.perception.show_tile(tile, **distortions)

    def show_troop(self, troop, **distortions):
        self.perception.show_troop(troop, **distortions)

    def do_turn(self, turn, events):
        self.current_turn = turn
        for event in events:
            event.trigger(self)
        self.events.clear()

    def end_turn(self):
        if self.troop and not self.troop.units:
            self.stop_actions()  # ToDo: check if this could potentially be called every turn; if so it's not good
            return
        if self.troop_target:
            if not self.troop_target.units:
                self.troop_target = None
            else:
                pos = self.troop_target.pos
                distance = maths.distance(pos, self.troop.pos)
                if math.ceil(distance) == 1:
                    self.walk_path.clear()
                    self.actions.append(Attack(self.troop.id, self.troop_target.id))
                else:
                    self.path_to(*pos)
        if self.walk_path:
            troop = self.troop
            x, y = self.walk_path.pop(0)
            if (x, y) in [t.pos for t in self.perception.troops.values() if t.units]:
                self.stop_actions()
            else:
                self.actions.append(Move(troop.id, x, y))
                self._discover((x, y))

    def path_to(self, x, y):
        def get_neighbors(x, y):
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if abs(a) + abs(b) != 1:
                        continue
                    yield x + a, y + b

        troop = self.troop
        start_pos = troop.x, troop.y
        end_pos = int(x), int(y)
        coord = pos_to_coord(*end_pos)
        try:
            tile = self.perception.tiles[coord]
        except KeyError:
            self.stop_actions()
            return
        if not tile.passable(troop):
            self.stop_actions()
            return

        open = {
            start_pos: {
                'parent': None,
                'g_cost': 0,
                'h_cost': maths.distance(end_pos, start_pos)
            }
        }
        closed = {}

        while True:
            if not open:
                self.stop_actions()
                return
            current = sorted(
                sorted(
                    open.items(),
                    key=lambda t: t[1]['h_cost']
                ),
                key=lambda t: t[1]['h_cost'] + t[1]['g_cost']
            )[0]
            current = current[0]
            closed[current] = open.pop(current)

            if current == end_pos:
                break

            for pos in get_neighbors(*current):
                g_cost = maths.distance(start_pos, pos)
                coords = pos_to_coord(*pos)
                if coords not in self.perception.tiles:
                    continue
                elif not self.perception.tiles[coords].passable(troop):
                    continue
                elif pos in closed:
                    continue
                elif pos not in open:
                    open[pos] = {
                        'parent': current,
                        'g_cost': g_cost,
                        'h_cost': maths.distance(end_pos, pos)
                    }
                elif g_cost < open[pos]['g_cost']:
                    open[pos]['g_cost'] = g_cost
                    open[pos]['parent'] = current

        path = []
        while current != start_pos:
            path.append(current)
            current = closed[current]['parent']

        self.walk_path = path[::-1]
