

from core.event import TileEvent


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
                info_update = TileEvent(
                    pos=tile.pos,
                    population=tile.population + increase
                )
                self.actions.append(info_update)

    def distribute_settlers(self):
        for dominion in self.perception.dominions.values():
            extra_population = 0
            for tile in dominion.tiles:
                settlers = max(0, tile.population - int(tile.fertility * .7))
                if settlers:
                    info_update = TileEvent(
                        pos=tile.pos,
                        population=tile.population - settlers
                    )
                    self.actions.append(info_update)
                    extra_population += settlers
            if not extra_population:
                continue

            tiles = self.perception.closest_tiles(
                dominion.capital.pos,
                lambda t: t.population <= int(t.fertility * .2)
            )
            for tile in tiles:
                possible_settlers = max(int(tile.fertility * .5) - tile.population, 0)
                settlers = min(possible_settlers, extra_population)
                if settlers:
                    info_update = TileEvent(
                        pos=tile.pos,
                        population=tile.population + settlers,
                        dominion_id=dominion.id
                    )
                    self.actions.append(info_update)
                    extra_population = extra_population - settlers
                    if not extra_population:
                        break
