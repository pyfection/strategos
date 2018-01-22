

import math

from helpers import maths
from helpers.convert import pos_to_coord
from core.event import Move, Attack
from core.mixins import EventResponseMixin


class Actor(EventResponseMixin):
    def __init__(self, name, entity_id=None, perception=None, events=None):
        self.name = name  # unique identifier / player/account name
        self.entity_id = entity_id
        self.perception = perception
        self.events = events or []  # events coming from outside
        self.pre_processing = []  # events caused by self
        self.action = None  # the one action self can do per turn
        self.walk_path = []
        self.troop_target = None  # troop target

    @property
    def entity(self):
        if self.perception:
            return self.perception.entities.get(self.entity_id)
        else:
            return None

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
        if self.troop_target:
            if not self.troop_target.units:
                self.troop_target = None
            else:
                pos = self.troop_target.pos
                distance = maths.distance(pos, self.entity.troop.pos)
                if math.ceil(distance) == 1:
                    self.walk_path.clear()
                    self.action = Attack(self.entity.troop.id, self.troop_target.id)
                else:
                    self.path_to(*pos)
        if self.walk_path:
            troop = self.entity.troop
            x, y = self.walk_path.pop(0)
            if (x, y) in [troop.pos for troop in self.perception.troops.values()]:
                self.stop_troop(self.entity.troop.id)
            else:
                self.action = Move(troop.id, x, y)

    def path_to(self, x, y):
        def get_neighbors(x, y):
            for a in range(-1, 2):
                for b in range(-1, 2):
                    if abs(a) + abs(b) != 1:
                        continue
                    yield x + a, y + b

        troop = self.entity.troop
        start_pos = troop.x, troop.y
        end_pos = int(x), int(y)
        coord = pos_to_coord(*end_pos)
        try:
            tile = self.perception.tiles[coord]
        except KeyError:
            self.walk_path.clear()
            return
        if not tile.passable(troop):
            self.walk_path.clear()
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
                break
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
