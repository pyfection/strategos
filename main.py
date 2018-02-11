

from threading import Thread
import ujson

from kivy.app import App

from core.world import World
from core.actor.visual import Visual
from core.actor.observer import Observer
from core.actor.ai import AI


class GameApp(App):
    title = "Strategos"

    def build(self):
        with open('scenarios/rise_of_bavaria/setup.json') as f:
            setup = ujson.load(f)
        actor = Visual(name='observer')
        ai1 = AI(name='testai1')
        # ai2 = AI(name='testai2', entity_id=list(setup['entities'].keys())[1])
        setup.update({
            'actors': [
                actor,
                ai1,
                # ai2
            ],
            'actor_to_entity_mapping': {
                actor.name: list(setup['entities'].keys())[0],
                ai1.name: list(setup['entities'].keys())[1]
            },
            'seed': 555
        })
        world = World(setup)
        view = actor.view
        t = Thread(target=world.run)
        t.start()
        return view


if __name__ == '__main__':
    GameApp().run()
