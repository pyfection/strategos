

from kivy.app import App
from kivy.clock import Clock

from core.world import World
from core.actor.visual import Visual


class GameApp(App):
    def build(self):
        world = World()
        actor = Visual(name='testplayer')
        world.load_map('2playertest')
        world.add_actor(actor)
        view = actor.view
        # Clock.schedule_interval(lambda dt: world.update(), .1)
        return view


if __name__ == '__main__':
    GameApp().run()
