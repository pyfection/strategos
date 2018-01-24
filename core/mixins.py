

class EventResponseMixin:
    perception = None
    troop_target = None
    troop = None
    walk_path = []

    def quit_actor(self, actor):
        pass

    def move_troop(self, troop_id, x, y):
        try:
            troop = self.perception.troops[troop_id]
        except KeyError:
            return
        if troop.units:
            troop.x, troop.y = x, y

    def stop_actions(self):
        self.troop_target = None
        self.walk_path.clear()

    def change_troop_unit_amount(self, troop_id, amount):
        troop = self.perception.troops[troop_id]
        troop.units += amount
        if troop.units <= 0:
            troop.units = 0
            if self.troop_target and troop_id == self.troop_target.id:
                self.stop_actions()
            elif self.troop and troop_id == self.troop.id:
                self.stop_actions()
