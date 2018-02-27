

import random

from helpers.maths import closest_tiles
from core.event import InformationUpdate


class DominionManager:
    BREED_MOD = .1

    def __init__(self, perception):
        self.perception = perception
        self.actions = []

    def do_turn(self):
        self.breed()
        self.distribute_settlers()

    def breed(self):
        for dominion in self.perception.dominions.values():
            for tile in dominion.tiles:
                women = tile.population // 2
                increase = women * tile.breed_mod
                if not increase:
                    continue
                info_update = InformationUpdate(
                    percept='tiles',
                    id=tile.pos,
                    updates={'population': tile.population + increase},
                    pos=tile.pos
                )
                self.actions.append(info_update)

    def distribute_settlers(self):
        for dominion in self.perception.dominions.values():
            extra_population = 0
            for tile in dominion.tiles:
                settlers = max(0, tile.population - tile.fertility)
                tile.population -= settlers
                extra_population += settlers
            if not extra_population:
                continue

            tiles = closest_tiles(
                dominion.capital.pos,
                self.perception.tiles,
                lambda t: t.population < t.fertility
            )
            for tile in tiles:
                settlers = tile.fertility - tile.population
                tile.population += min(settlers, extra_population)
                tile.dominion = dominion
                extra_population = max(extra_population - settlers, 0)
                if not extra_population:
                    break
