

from controller.update import ACTOR, TILE
from controller.actor import Actor


class AI(Actor):
    def act(self, update, callback):
        for i, tile in enumerate(self.owned_tiles, 1):
            update.add(
                obj=TILE,
                identifiers={'x': tile.x, 'y': tile.y},
                changes={'units': tile.units+1}
            )
            if self.unplaced_units == i:
                break
        update.add(
            obj=ACTOR,
            identifiers={'name': self.name},
            changes={'unplaced_units': 0}
        )
        callback(update)


Actor.TYPES['ai'] = AI
