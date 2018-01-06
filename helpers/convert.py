

def pos_to_coord(x, y):
    return f'{x}|{y}'

def coord_to_pos(coord):
    return tuple(map(int, coord.split('|')))