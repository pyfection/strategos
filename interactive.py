

from model.base import db
from controller.world import World
from controller.actor import Actor
from controller.tile import Tile


"""
start like this:
>>> python -i interactive.py
"""


db.load_game('strategos_test')
world = World()
p1 = Actor(name="John")
p2 = Actor(name="Jane")
world.generate_terrain()
world.distribute_tiles()
