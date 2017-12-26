

from controller.world import World
from controller.actor import Actor
from controller.tile import Tile


"""
start like this:
>>> python -i interactive.py
"""


world = World(game_name='strategos_test')
p1 = Actor(name="John")
p2 = Actor(name="Jane")
world.generate_terrain()
world.distribute_tiles()
print("Following objects are ready:")
print(' '.join([o for o in dir() if not o.startswith('_')]))