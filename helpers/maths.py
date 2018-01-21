

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


if __name__ == '__main__':
    print(limit_distance((1, 1), (10, 15), 5))