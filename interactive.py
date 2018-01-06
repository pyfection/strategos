

import random
from threading import Thread

from core.world import World
from core.actor.terminal import Terminal

"""
start like this:
>>> python -i interactive.py
"""

while True:
    mos = input("load from 'map' or 'save': ")
    if mos in ('map', 'save'):
        break
    else:
        print("Input needs to be 'map' or 'save'")

if mos == 'map':
    world = World(seed=random.randint(0, 1000))
    world.load_map('2playertest')
elif mos == 'save':
    world = World.load_savegame('testgame')
else:
    raise EnvironmentError("Should not get here")

self = Terminal(name="John")
world.add_actor(self)

if mos == 'map':
    world.distribute_settlements()


main_thread = Thread(target=world.run)
main_thread.start()
