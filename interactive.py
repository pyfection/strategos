

from threading import Thread

from core.world import World
from core.actor.terminal import Terminal
from core.event import Quit

"""
start like this:
>>> python -i interactive.py
"""


world = World()
world.load_map('2playertest')
self = Terminal(name="John")
world.actors.append(self)
world.distribute_settlements()
main_thread = Thread(target=world.run)
main_thread.start()
