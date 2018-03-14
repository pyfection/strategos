

class EventResponseMixin:
    perception = None
    troop_target = None
    troop = None
    walk_path = []

    def quit_actor(self, event):
        return

    def move_troop(self, event):
        return

    def attack_troop(self, event):
        return

    def update_perception(self, event):
        percept = getattr(self.perception, event.percept)
        for name, value in event.updates.items():
            setattr(percept[event.id], name, value)
