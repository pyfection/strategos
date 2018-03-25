

import random
from uuid import uuid4

from core.perception.troop import Troop

class classproperty(property):
    def __get__(self, cls, owner):
        return max([d.importance for d in owner.dependencies], default=0)


class Event:
    dependencies = ()

    @classproperty
    def importance(cls):
        return


class Quit(Event):
    dependencies = ()

    def __init__(self, actor):
        self.actor = actor  # actor to be quit

    def trigger(self, reactor):
        reactor.on_actor_quit(self.actor)


class TroopEvent(Event):
    def __init__(self, id, name=None, leader_id=None, units=None, experience=None, pos=None, view_range=None):
        self.id = id
        self.name = name
        self.leader_id = leader_id
        self.units = units
        self.experience = experience
        self.pos = pos
        self.view_range = view_range

    def trigger(self, reactor):
        reactor.on_troop_update(self)

        if self.name is not None:
            reactor.on_troop_name(self.id, self.name)
        if self.pos is not None:
            reactor.on_troop_pos(self.id, self.pos)
        if self.leader_id is not None:
            reactor.on_troop_leader_id(self.id, self.leader_id)
        if self.units is not None:
            reactor.on_troop_units(self.id, self.units)
        if self.experience is not None:
            reactor.on_troop_experience(self.id, self.experience)
        if self.view_range is not None:
            reactor.on_troop_view_range(self.id, self.view_range)


class TileEvent(Event):
    def __init__(self, pos, z=None, dominion_id=None, population=None, base_fertility=None, type=None):
        self.pos = pos
        self.z = z
        self.dominion_id = dominion_id
        self.population = population
        self.base_fertility = base_fertility
        self.type = type

    def trigger(self, reactor):
        reactor.on_tile_update(self)

        if self.z is not None:
            reactor.on_tile_z(self.pos, self.z)
        if self.dominion_id is not None:
            reactor.on_tile_dominion_id(self.pos, self.dominion_id)
        if self.population is not None:
            reactor.on_tile_population(self.pos, self.population)
        if self.base_fertility is not None:
            reactor.on_tile_base_fertility(self.pos, self.base_fertility)


class Attack(Event):
    STRENGTH_MOD = .1
    dependencies = ()

    def __init__(self, attacker_id, defender_id):
        super().__init__()
        self.attacker_id = attacker_id
        self.defender_id = defender_id

    def trigger(self, reactor):
        reactor.on_troop_attack(self.attacker_id, self.defender_id, self.STRENGTH_MOD)
