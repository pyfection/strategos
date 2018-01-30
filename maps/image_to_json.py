

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__name__)))

import ujson

from helpers.loader import load_map


map_name = sys.argv[1]
result = load_map(map_name)
with open(f'{map_name}.json', 'w') as f:
    f.write(ujson.dumps(result, indent=2))
