

from controller.actor.world import World
from controller.actor.ai import AI
from controller.actor.terminal import Terminal

"""
start like this:
>>> python -i interactive.py
"""


world = World(game_name='strategos_test')
p1 = Terminal(name="John")
p2 = AI(name="Jane")
world.generate_terrain()
world.distribute_tiles()
world.run()
