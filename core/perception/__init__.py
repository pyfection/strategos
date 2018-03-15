

from core.perception.entity import Entity
from core.perception.faction import Faction
from core.perception.tile import TILE_TYPES, Grass
from core.perception.troop import Troop
from core.perception.dominion import Dominion
from maps import MapLoader
from helpers.convert import coord_to_pos
from helpers.maths import pos_neighbors


class Perception:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.entities = {}
        self.tiles = {}
        self.troops = {}
        self.factions = {}
        self.dominions = {}
        self.map_loader = None

    @property
    def entity(self):
        return self.entities.get(self.entity_id)

    @property
    def troop(self):
        entity = self.entity
        if entity:
            return entity.troop

    @classmethod
    def load(cls, dictionary, entity_id=None):
        self = cls(entity_id)
        if 'map_name' in dictionary:
            self.map_loader = MapLoader(dictionary['map_name'], dictionary['seed'])

        for entity_id, entity_dict in dictionary.get('entities', dict()).items():
            Entity(self, id=entity_id, **entity_dict)

        if self.entity_id and self.entity_id not in self.entities:
            raise KeyError("The entity of the perception is not in its perceived entities")

        for tile_coord, tile_dict in dictionary.get('tiles', dict()).items():
            x, y = coord_to_pos(tile_coord)
            Tile = TILE_TYPES[tile_dict.pop('type', 'grass')]
            Tile(self, x=x, y=y, **tile_dict)

        for troop_id, troop_dict in dictionary.get('troops', dict()).items():
            Troop(self, id=troop_id, **troop_dict)

        for faction_id, faction_dict in dictionary.get('factions', dict()).items():
            Faction(self, id=faction_id, **faction_dict)

        for dominion_id, dominion_dict in dictionary.get('dominions', dict()).items():
            capital = coord_to_pos(dominion_dict.pop('capital_pos'))
            Dominion(self, id=dominion_id, capital_pos=capital, **dominion_dict)

        return self

    def get_tile(self, x, y):
        try:
            tile = self.tiles[(x, y)]
        except KeyError:
            if self.map_loader:
                TileType, kwargs = self.map_loader.get_tile(x, y)
                tile = TileType(self, **kwargs)
            else:
                raise AttributeError("This perception does not have a map loader")
        return tile

    def closest_tiles(self, start_pos, condition):
        checked = []
        current = set(pos_neighbors(start_pos))
        next = set()
        while True:
            for pos in current:
                if pos in checked:
                    continue

                checked.append(pos)

                tile = self.get_tile(*pos)
                if not tile.passable:
                    continue

                for neighbor in pos_neighbors(pos):
                    next.add(neighbor)

                if condition(tile):
                    yield tile

            current = next.copy()
            next.clear()
