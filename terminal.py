

from core.actor.ai import AI
from core.actor.terminal import Terminal
from core.world import World

world = World(game_name='strategos_test')
p1 = Terminal(name="John")
p2 = AI(name="Jane")
world.generate_terrain()
world.distribute_tiles()
world.run()
