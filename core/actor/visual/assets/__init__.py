

import os

from kivy.uix.image import Image


ASSET_PATH = os.path.dirname(__file__)

tiles = {
    'grass': Image(source=os.path.join(ASSET_PATH, "tiles", "grass.png")),
    'settlement': Image(source=os.path.join(ASSET_PATH, "tiles", "settlement.png")),
}
