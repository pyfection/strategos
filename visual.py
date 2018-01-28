

from threading import Thread
from uuid import uuid4

from kivy.app import App

from helpers.loader import load_map
from core.world import World
from core.actor.visual import Visual
from core.actor.observer import Observer
from core.actor.ai import AI


class GameApp(App):
    def build(self):
        entity_id = uuid4()
        troop_id = uuid4()
        actor = Observer(name='observer')
        ai = AI(name='testplayer', entity_id=entity_id)
        tiles = load_map('2playertest')
        tiles['18|27']['population'] = 100
        tiles['30|24']['population'] = 100
        setup = {
            'tiles': tiles,
            'actors': [
                actor,
                ai
            ],
            'entities': {
                entity_id: {
                    'name': 'testentity',
                    'ruler': None,
                    'troop': troop_id,
                }
            },
            'factions': {
                uuid4(): {
                    'name': 'testfaction',
                    'leader': entity_id,
                }
            },
            'troops': {
                troop_id: {
                    'name': 'testtroop',
                    'units': 10,
                    'experience': 1,
                    'x': 18,
                    'y': 28
                }
            },
            'seed': 555
        }
        world = World(setup)
        # world.assign_entities_to_actors()
        # world.distribute_settlements()
        # world.reveal_all_tiles()
        # world.assign_troops_to_actors()
        # world.reveal_all_troops()
        view = actor.view
        t = Thread(target=world.run)
        t.start()
        return view


if __name__ == '__main__':
    GameApp().run()
