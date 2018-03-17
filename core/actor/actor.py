

import math

from helpers import maths
from core.event import Move, Attack
from core.mixins import EventResponseMixin


class ActorEventResponseMixin(EventResponseMixin):
    def update_perception(self, event):
        if event.percept == 'troops':
            if event.id not in self.perception.troops:
                self.on_troop_discover(event)

            for key, value in event.updates.items():
                if key == 'units':
                    self.on_troop_units_update(event.id, value)
                elif key == 'pos':
                    self.on_troop_pos_update(event.id, value)
        super().update_perception(event)

    def on_troop_discover(self, event):
        return

    def on_troop_units_update(self, id, value):
        troop = self.perception.troops[id]
        if troop.units <= 0:
            if self.troop_target and id == self.troop_target.id:
                self.stop_actions()
            elif self.troop and id == self.troop.id:
                self.stop_actions()

    def on_troop_pos_update(self, id, pos):
        troop = self.perception.troops[id]
        troop.pos = pos


class Actor(ActorEventResponseMixin):
    def __init__(self, name, perception=None, events=None):
        self.name = name  # unique identifier / player/account name
        self.perception = perception
        self.events = events or []  # events coming from outside
        self.actions = []  # actions (events) actor wants to do
        self.walk_path = []
        self.troop_target_id = None  # troop target

    def setup(self):
        pass

    @property
    def entity(self):
        if self.perception:
            return self.perception.entity

    @property
    def troop(self):
        entity = self.entity
        if entity:
            return entity.troop

    @property
    def troop_target(self):
        try:
            return self.perception.troops[self.troop_target_id]
        except KeyError:
            return None

    @troop_target.setter
    def troop_target(self, troop):
        if troop is None:
            self.troop_target_id = None
        else:
            self.troop_target_id = troop.id

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
        try:
            tile = self.perception.tiles[end_pos]
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
                if pos not in self.perception.tiles:
                    continue
                elif not self.perception.tiles[pos].passable(troop):
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

    def stop_actions(self):
        self.troop_target = None
        self.walk_path.clear()