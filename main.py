

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock

from view.game_frame import GameFrame
from controller.actor import Actor
from controller.world import World
from model.base import db


class GameApp(App):
    def build(self):
        world = World()
        entities = [{
            'name': 'Testplayer',
            'unit': 'cavalry',
            'color': '0 .6 .5 .5',
        }]
        game_name = 'testgame'
        db.load_game(game_name)
        for attributes in entities:
            entity = world.add_entity(**attributes)
            actor = Actor(world=world, entity_ref=entity.id)
            world.actors[id(actor)] = actor
        world.setup()
        view = GameFrame(actor)
        Clock.schedule_interval(lambda dt: world.update(), .1)
        return view


if __name__ == '__main__':
    GameApp().run()
