import random
WINDOW_WIDTH = 570
WINDOW_HEIGHT = 300
TILE_SIZE = 30


def generate_wall_map():
    """
    Generates wall map for level 1.
    """
    _list = [[0 for x in range(0, WINDOW_WIDTH, TILE_SIZE)] for y in range(0, WINDOW_HEIGHT, TILE_SIZE)]
    for index_y in range(len(_list)):
        for index_x in range(len(_list[index_y])):
            if index_x % 2 == 1:
                if index_y % 2 == 1:
                    _list[index_y][index_x] = index_x
                if index_y == 5:
                    _list[index_y][index_x] = 0
    return _list

WALL_MAP = generate_wall_map()


def generate_none_treasure_map():
    """
    Generates treasures that buff nothing (only breakable wall)
    for level 1.
    """
    _list = [[None for x in range(0, WINDOW_WIDTH+TILE_SIZE, TILE_SIZE)] for y in range(0, WINDOW_HEIGHT+TILE_SIZE, TILE_SIZE)]
    for index_y in range(len(_list)):
        for index_x in range(len(_list[index_y])):
            if index_y == 0:
                if index_x > 5:
                    _list[index_y][index_x] = index_x
            if index_y == 1:
                if index_x > 0 and index_x % 2 == 0:
                    _list[index_y][index_x] = index_x
            if index_y == 2:
                if index_x > 0:
                    _list[index_y][index_x] = index_x
            if index_y == 3 or index_y == 7:
                if index_x % 2 == 0:
                    _list[index_y][index_x] = index_x
            if index_y == 4 or index_y == 6:
                _list[index_y][index_x] = index_x
            if index_y == 5:
                _list[index_y][index_x] = None
            if index_y == 8:
                if index_x < 18:
                    _list[index_y][index_x] = index_x
            if index_y == 9:
                if index_x < 18 and index_x % 2 == 0:
                    _list[index_y][index_x] = index_x
            if index_y == 10:
                if index_x < 13:
                    _list[index_y][index_x] = index_x
    return _list

NONE_MAP = generate_none_treasure_map()


def generate_el_treasure_map():
    """
    Generates extra live map for level 1.
    """
    _list = [[None for x in range(0, WINDOW_WIDTH, TILE_SIZE)] for y in range(0, WINDOW_HEIGHT, TILE_SIZE)]
    numbers = 2
    for number in range(numbers):
        y = random.randrange(len(_list))
        x = random.randrange(len(_list[0]))
        while NONE_MAP[y][x] is None:
            y = random.randrange(len(_list))
            x = random.randrange(len(_list[0]))
        _list[y][x] = x
    return _list

EL_MAP = generate_el_treasure_map()


def generate_ee_treasure_map():
    """
    Generates extra explode map for level 1.
    """
    _list = [[None for x in range(0, WINDOW_WIDTH, TILE_SIZE)] for y in range(0, WINDOW_HEIGHT, TILE_SIZE)]
    numbers = 3
    for number in range(numbers):
        y = random.randrange(len(_list))
        x = random.randrange(len(_list[0]))
        while NONE_MAP[y][x] is None and EL_MAP[y][x] is None:
            y = random.randrange(len(_list))
            x = random.randrange(len(_list[0]))
        _list[y][x] = x
    return _list

EE_MAP = generate_ee_treasure_map()


def generate_key_treasure_map():
    """
    Generates key map for level 1.
    """
    _list = [[None for x in range(0, WINDOW_WIDTH, TILE_SIZE)] for y in range(0, WINDOW_HEIGHT, TILE_SIZE)]
    numbers = 2
    for number in range(numbers):
        y = random.randrange(len(_list))
        x = random.randrange(len(_list[0]))
        while NONE_MAP[y][x] is None and EL_MAP[y][x] is None and EE_MAP[y][x] is None:
            y = random.randrange(len(_list))
            x = random.randrange(len(_list[0]))
        _list[y][x] = x
    return _list

KEY_MAP = generate_key_treasure_map()