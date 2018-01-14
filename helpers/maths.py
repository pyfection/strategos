

from math import hypot


def limit_distance(start, end, limit):
    x1, y1 = start
    x2, y2 = end
    dist = hypot(x2 - x1, y2 - y1)
    percent = limit / dist
    return x1 + ((x2 - x1) * percent), y1 + ((y2 - y1) * percent)


if __name__ == '__main__':
    print(limit_distance((1, 1), (10, 15), 5))
