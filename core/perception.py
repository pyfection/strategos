

from helpers.convert import pos_to_coord, coord_to_pos
from core.entity import Entity
from core.tile import TILE_TYPES
from core.troop import Troop
from core.faction import Faction


class Perception:
    def __init__(self):
        self.entities = {}
        self.tiles = {}
        self.troops = {}
        self.factions = {}

    @classmethod
    def load(cls, dictionary):
        self = cls()
        for entity_id, entity_dict in dictionary.get('entities', dict()).items():
            perception = cls.load(entity_dict)
            entity = Entity(
                id=entity_id,
                name=entity_dict.get('name'),
                perception=perception
            )
            self.entities[entity_id] = entity

        for tile_coord, tile_dict in dictionary.get('tiles', dict()).items():
            x, y = coord_to_pos(tile_coord)
            owner_id = tile_dict.get('owner')
            owner = self.entities.get(owner_id)
            Tile = TILE_TYPES[tile_dict.get('type', 'grass')]
            tile = Tile(x=x, y=y, z=tile_dict.get('z', 0), owner=owner)
            self.tiles[tile_coord] = tile

        for troop_id, troop_dict in dictionary.get('troops', dict()).items():
            troop = Troop(id=troop_id, **troop_dict)
            self.troops[troop_id] = troop

        for faction_id, faction_dict in dictionary.get('factions', dict()).items():
            leader = self.entities[faction_dict['leader']]
            faction = Faction(
                id=faction_id,
                name=faction_dict['name'],
                leader=leader
            )
            self.factions[faction_id] = faction

        for entity_id, entity in self.entities.items():
            troop_id = dictionary['entities'][entity_id].get('troop')
            entity.troop = self.troops.get(troop_id)
            ruler_id = dictionary['entities'][entity_id].get('ruler')
            entity.ruler = self.entities.get(ruler_id)

        return self

    def show_tile(self, tile, **distortions):
        self.tiles[pos_to_coord(tile.x, tile.y)] = tile.copy(**distortions)

    def show_entity(self, entity, **distortions):
        self.entities[entity.id] = entity.copy(**distortions)

    def show_troop(self, troop, **distortions):
        try:
            old_troop = self.troops[troop.id]
        except KeyError:
            self.troops[troop.id] = troop.copy(**distortions)
        else:
            old_troop.update(troop, **distortions)

    def show_faction(self, faction, **distortions):
        self.factions[faction.id] = faction.copy(**distortions)
