

from core.perception.troop import Troop
from core.perception.tile import TILE_TYPES


class Reactor:
    def __init__(self, actor):
        self.actor = actor

    def on_actor_quit(self, actor):
        return

    def on_troop_update(self, id):
        return

    def on_troop_move(self, troop_id, pos):
        self.on_troop_pos(troop_id, pos)

    def on_troop_attack(self, attacker_id, defender_id, strength_mod):
        return

    def on_troop_rest(self, id):
        return

    def on_troop_pos(self, id, pos):
        return

    def on_troop_name(self, id, name):
        return

    def on_troop_units(self, id, units):
        return

    def on_troop_leader_id(self, id, leader_id):
        return

    def on_troop_experience(self, id, experience):
        return

    def on_troop_vigor(self, id, vigor):
        return

    def on_troop_view_range(self, id, view_range):
        return

    def on_tile_update(self, pos):
        return

    def on_tile_z(self, pos, z):
        return

    def on_tile_dominion_id(self, pos, dominion_id):
        return

    def on_tile_population(self, pos, population):
        return

    def on_tile_base_fertility(self, pos, base_fertility):
        return


class PerceptionReact(Reactor):
    def on_troop_update(self, event):
        if event.id not in self.actor.perception.troops:
            Troop(self.actor.perception, id=event.id)

    def on_troop_pos(self, id, pos):
        troop = self.actor.perception.troops[id]
        troop.pos = pos

    def on_troop_name(self, id, name):
        troop = self.actor.perception.troops[id]
        troop.name = name

    def on_troop_leader_id(self, id, leader_id):
        troop = self.actor.perception.troops[id]
        troop.leader_id = leader_id

    def on_troop_units(self, id, units):
        troop = self.actor.perception.troops[id]
        troop.units = units

    def on_troop_experience(self, id, experience):
        troop = self.actor.perception.troops[id]
        troop.experience = experience

    def on_troop_vigor(self, id, vigor):
        troop = self.actor.perception.troops[id]
        troop.vigor = vigor

    def on_troop_view_range(self, id, view_range):
        troop = self.actor.perception.troops[id]
        troop.view_range = view_range

    def on_tile_update(self, event):
        if event.pos not in self.actor.perception.tiles:
            x, y = event.pos
            Tile = TILE_TYPES[event.type]
            Tile(self.actor.perception, x, y)

    def on_tile_z(self, pos, z):
        tile = self.actor.perception.tiles[pos]
        tile.z = z

    def on_tile_dominion_id(self, pos, dominion_id):
        tile = self.actor.perception.tiles[pos]
        tile.dominion_id = dominion_id

    def on_tile_population(self, pos, population):
        tile = self.actor.perception.tiles[pos]
        tile.population = population

    def on_tile_base_fertility(self, pos, base_fertility):
        tile = self.actor.perception.tiles[pos]
        tile.base_fertility = base_fertility
