

class EventResponseMixin:
    perception = None
    troop_target = None

    def quit_actor(self, actor):
        pass

    def move_troop(self, troop_id, x, y):
        try:
            troop = self.perception.troops[troop_id]
        except KeyError:
            return
        if troop.units:
            troop.x, troop.y = x, y

    def change_troop_unit_amount(self, troop_id, amount):
        troop = self.perception.troops[troop_id]
        troop.units += amount
        if troop.units <= 0:
            troop.units = 0
            if self.troop_target and troop_id == self.troop_target.id:
                self.troop_target = None