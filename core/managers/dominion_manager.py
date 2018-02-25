

import random

from helpers.maths import closest_tiles


class DominionManager:
    BREED_MOD = .1

    def __init__(self, perception):
        self.perception = perception

    def do_turn(self):
        self.breed()
        self.distribute_settlers()

    def breed(self):
        for dominion in self.perception.dominions.values():
            for tile in dominion.tiles:
                women = tile.population // 2
                increase = 0
                for b in range(women):
                    if random.random() < self.BREED_MOD:
                        increase += 1
                tile.population += increase

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
                extra_population = max(extra_population - settlers, 0)
                if not extra_population:
                    break
