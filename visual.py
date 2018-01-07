

from threading import Thread

from kivy.app import App

from core.world import World
from core.actor.visual import Visual


class GameApp(App):
    def build(self):
        world = World()
        actor = Visual(name='testplayer')
        world.load_map('2playertest')
        world.add_actor(actor)
        world.distribute_settlements()
        view = actor.view
        t = Thread(target=world.run)
        t.start()
        return view


if __name__ == '__main__':
    GameApp().run()
