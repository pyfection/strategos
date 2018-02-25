

from helpers.maths import closest_tiles


class DominionManager:
    def __init__(self, perception):
        self.perception = perception

    def do_turn(self):
        self.distribute_settlers()

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
