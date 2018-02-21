

from core.perception.entity import Entity
from core.perception.faction import Faction
from core.perception.tile import TILE_TYPES
from core.perception.troop import Troop
from core.perception.dominion import Dominion
from helpers.convert import pos_to_coord, coord_to_pos


class Perception:
    def __init__(self, entity_id):
        self.entity_id = entity_id
        self.entities = {}
        self.tiles = {}
        self.troops = {}
        self.factions = {}
        self.dominions = {}

    @property
    def entity(self):
        return self.entities.get(self.entity_id)

    @classmethod
    def load(cls, dictionary, entity_id=None):
        self = cls(entity_id)

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
            Dominion(self, id=dominion_id, **dominion_dict)

        return self

    def show_tile(self, tile):
        self.tiles[pos_to_coord(tile.x, tile.y)] = tile.copy(self)

    def show_entity(self, entity):
        self.entities[entity.id] = entity.copy(self)

    def show_troop(self, troop):
        try:
            old_troop = self.troops[troop.id]
        except KeyError:
            self.troops[troop.id] = troop.copy(self)
        else:
            old_troop.update(troop)

    def show_faction(self, faction):
        self.factions[faction.id] = faction.copy(self)
