

from math import hypot


def distance(start, end):
    x1, y1 = start
    x2, y2 = end
    return hypot(x2 - x1, y2 - y1)


def limit_distance(start, end, limit):
    dist = distance(start, end)
    percent = min(limit / dist, 1)
    x1, y1 = start
    x2, y2 = end
    return x1 + ((x2 - x1) * percent), y1 + ((y2 - y1) * percent)


def mean(*numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


def pos_neighbors(pos):
    x, y = pos
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]


def closest_tiles(start_pos, tiles, condition):
    checked = []
    current = set(pos_neighbors(start_pos))
    next = set()
    while True:
        for pos in current:
            if pos in checked:
                continue

            checked.append(pos)

            tile = tiles[pos]
            if not tile.passable:
                continue

            for neighbor in pos_neighbors(pos):
                next.add(neighbor)

            if condition(tile):
                yield tile

        current = next.copy()
        next.clear()


if __name__ == '__main__':
    print(limit_distance((1, 1), (10, 15), 5))
