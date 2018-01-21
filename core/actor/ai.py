

import random

from core.actor.actor import Actor


class AI(Actor):
    def do_turn(self, turn, events):
        super().do_turn(turn, events)

        if not self.walk_path:
            troop = self.entity.troop
            tiles = list(filter(lambda t: t.passable(troop), self.perception.tiles.values()))
            tile = random.choice(tiles)
            x, y = tile.x, tile.y
            self.path_to(x, y)
        self.end_turn()
