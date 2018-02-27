

from uuid import uuid4

from core.event import Quit, Move, Attack, SpawnTroop, Uncover, Discover
from helpers.maths import distance


class EventResponseMixin:
    perception = None
    troop_target = None
    troop = None
    walk_path = []

    def quit_actor(self, event):
        actor = event.actor

    def move_troop(self, event):
        try:
            troop = self.perception.troops[event.troop_id]
        except KeyError:
            return
        if troop.units:
            troop.x, troop.y = event.x, event.y

    def attack_troop(self, event):
        self.change_troop_unit_amount(event.defender_id, event.reduce_amount)

    def discover_troop(self, event):
        self.show_troop(event.troop)

    def uncover_tile(self, event):
        self.show_tile(event.tile)

    def stop_actions(self):
        self.troop_target = None
        self.walk_path.clear()

    def update_info(self, event):
        percept = getattr(self.perception, event.percept)
        for name, value in event.updates.items():
            setattr(percept[event.id], name, value)

    def change_troop_unit_amount(self, troop_id, amount):
        troop = self.perception.troops[troop_id]
        troop.units += amount
        if troop.units <= 0:
            troop.units = 0
            if self.troop_target and troop_id == self.troop_target.id:
                self.stop_actions()
            elif self.troop and troop_id == self.troop.id:
                self.stop_actions()


class EventDistortedResponseMixin(EventResponseMixin):
    pass


class EventProcessMixin(EventResponseMixin):
    def add_event_to_actor(self, event, actor):
        self.events.setdefault(actor.name, []).append(event)

    def quit_actor(self, event):
        from core.actor.ai import AI
        actor = event.actor
        self.actors.remove(actor)
        replacement = AI(
            name=str(uuid4()),
            perception=actor.perception,
            events=actor.events
        )
        self.actors.append(replacement)
        event = Quit(actor)
        for actor in self.actors:
            self.add_event_to_actor(event, actor)

    def move_troop(self, event):
        if (event.x, event.y) not in [troop.pos for troop in self.perception.troops.values() if troop.units]:
            super().move_troop(event)
            discover = Discover(troop=self.perception.troops[event.troop_id])
            for actor in self.actors:
                if actor.troop and actor.troop.in_view_range(event.x, event.y):
                    if event.troop_id in actor.perception.troops:
                        self.add_event_to_actor(event, actor)
                    else:
                        self.add_event_to_actor(discover, actor)

    def attack_troop(self, event):
        attacker = self.perception.troops[event.attacker_id]
        defender = self.perception.troops[event.defender_id]
        if defender.units == 0 or attacker.units == 0:
            return

        base = attacker.units * event.STRENGTH_MOD
        unit_ratio = attacker.units / defender.units  # attacker to defender ratio
        exp_ratio = attacker.experience / defender.experience
        effect = event.effectiveness_modifier
        kills = round(max(base * unit_ratio * exp_ratio * effect, 1))
        event.reduce_amount = -min(kills, defender.units)
        defender.units += event.reduce_amount

        for actor in self.actors:
            if actor.troop and actor.troop.in_view_range(defender.x, defender.y):
                self.add_event_to_actor(event, actor)

    def discover_troop(self, event):
        raise NotImplementedError("This event should not be triggered by a EventProcessMixin subclass")

    def uncover_tile(self, event):
        event.tile = self.get_tile(event.x, event.y)
        self.add_event_to_actor(event, event.requester)
        for troop_id, troop in self.perception.troops.items():
            if event.requester.troop and event.requester.troop.id == troop_id:
                continue
            if troop.pos == (event.x, event.y):
                discover = Discover(troop=troop)
                self.add_event_to_actor(discover, event.requester)  # ToDo: does this not just add updates to the same actor multiple times?

    def update_info(self, event):
        for actor in self.actors:
            troop = actor.troop
            if troop.in_view_range(event.x, event.y):
                self.add_event_to_actor(event, actor)
