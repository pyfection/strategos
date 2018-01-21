

from helpers import maths
from helpers.convert import pos_to_coord
from core.event import Move
from helpers.maths import distance, limit_distance


class Actor:
    def __init__(self, name, entity_id=None, perception=None, events=None):
        self.name = name  # unique identifier / player/account name
        self.entity_id = entity_id
        self.perception = perception
        self.events = events or []  # events coming from outside
        self.pre_processing = []  # events caused by self
        self.action = None  # the one action self can do per turn
        self.walk_path = []

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
        if self.walk_path:
            troop = self.entity.troop
            x, y = self.walk_path.pop(0)
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
        if not self.perception.tiles[pos_to_coord(*end_pos)].passable(troop):
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

    def move_troop(self, troop_id, x, y):
        try:
            troop = self.perception.troops[troop_id]
        except KeyError:
            return
        else:
            troop.x, troop.y = x, y

    def quit_actor(self, actor):
        pass
