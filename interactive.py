

from controller.world import World
from controller.actor import AI
from controller.tile import Tile


"""
start like this:
>>> python -i interactive.py
"""


world = World(game_name='strategos_test')
p1 = AI(name="John")
p2 = AI(name="Jane")
world.generate_terrain()
world.distribute_tiles()
print("Following objects are ready:")
print(' '.join([o for o in dir() if not o.startswith('_')]))
