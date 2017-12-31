

from threading import Thread

from model.base import db
from controller.actor.actor import Actor
from controller.actor.ai import AI
from controller.tile import Tile
from controller.event import Event


class World(Actor):
    NAME = '__world__'
    def __init__(self, game_name=None, **kwargs):
        if game_name:
            db.load_game(game_name)
        super(World, self).__init__(name=self.NAME, **kwargs)

    @property
    def is_running(self):
        return any([a for a in Actor.all() if a != self and not isinstance(a, AI)])

    def generate_terrain(self, width=10, height=10):
        for x in range(width):
            for y in range(height):
                Tile(x=x, y=y, owner=None, perceiver=self)

    def distribute_tiles(self):
        actors = [a for a in Actor.all() if a != self]
        undistributed = Tile.find(owner=None)
        while undistributed:
            for actor in actors:
                tile = undistributed.pop(0)
                tile.owner = actor
                tile.units = 1
                tile.copy(perceiver=actor)

    def do_turn(self, turn):
        super().do_turn(turn)
        # ToDo: add world specific events such as tile type changes
        pass

    def run(self):
        while self.is_running:
            actors = Actor.all()
            threads = []

            # Tell actors to update
            for actor in actors:
                t = Thread(target=actor.do_turn, kwargs={'turn': self.current_turn})
                threads.append(t)
                t.start()

            # Wait for all actors to finish
            for thread in threads:
                thread.join()

            # Apply accumulated updates and inform other actors about updates
            for event in Event.find(turn=self.current_turn):
                for actor in actors:
                    if event.causer != actor:
                        new_event = event.copy(perceiver=actor)
                        new_event.trigger()
                    else:
                        event.trigger()

            self.current_turn += 1


Actor.TYPES['world'] = World
