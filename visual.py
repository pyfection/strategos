

from threading import Thread
from uuid import uuid4

from kivy.app import App

from helpers.loader import load_map
from core.world import World
from core.actor.visual import Visual


class GameApp(App):
    def build(self):
        actor = Visual(name='testplayer')
        setup = {
            'tiles': load_map('2playertest'),
            'actors': [
                actor
            ]
        }
        world = World(setup)
        world.assign_entities_to_actors()
        world.distribute_settlements()
        world.assign_troops_to_actors()
        world.reveal_all_tiles()
        view = actor.view
        t = Thread(target=world.run)
        t.start()
        return view


if __name__ == '__main__':
    GameApp().run()
