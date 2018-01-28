

from threading import Thread
from uuid import uuid4

from kivy.app import App

from helpers.loader import load_map
from core.world import World
from core.actor.visual import Visual
from core.faction import Faction


class GameApp(App):
    def build(self):
        entity_id = uuid4()
        actor = Visual(name='testplayer', entity_id=entity_id)
        tiles = load_map('2playertest')
        tiles['18|27']['population'] = 100
        tiles['30|24']['population'] = 100
        setup = {
            'tiles': tiles,
            'actors': [
                actor
            ],
            'entities': {
                entity_id: {
                    'name': 'testentity',
                    'ruler': None,
                    'troop': None,
                }
            },
            'factions': {
                uuid4(): {
                    'name': 'testfaction',
                    'leader': entity_id,
                }
            },
            'seed': 555
        }
        world = World(setup)
        world.assign_entities_to_actors()
        world.reveal_all_tiles()
        world.reveal_all_troops()
        # world.distribute_settlements()
        world.assign_troops_to_actors()
        view = actor.view
        t = Thread(target=world.run)
        t.start()
        return view


if __name__ == '__main__':
    GameApp().run()
