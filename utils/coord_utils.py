from random import randint
from Constants.mosaic_settings import DIVIDER

def first_coord_change(coord: int, delta: int) -> int:
    """
    Method change coordinate from first pair of coordinates of rectangle with delta.

    :param coord - coordinate
    :param delta - delta
    :return coord
    """
    if coord - delta >= 0:
        out_coord = coord - randint(0, delta)
    else:
        out_coord = coord - randint(0, coord)
    return out_coord

def second_coord_change(coord: int, delta: int, size: int) -> int:
    """
    Method change coordinate from second pair of coordinates of rectangle with delta.

    :param coord - coordinate
    :param delta - delta
    :param size - size of image in this demention
    :return coord
    """
    if coord + delta <= size - 1:
        out_coord = coord + randint(0, delta)
    else:
        if size - coord <= 0:
            out_coord = coord
        else:
            out_coord = coord + randint(0, size - coord)
    return out_coord

def first_coord_change_for_bb(coord: int, size: int):
    """
    Method change coordinate from first pair of coordinates of rectangle on a random lesser values.

    :param coord - coordinate
    :param size - size of target box
    :return coord
    """
    if coord - size // DIVIDER > 0:
        coord -= randint(0, size // DIVIDER)
    else:
        coord -= randint(0, coord)
    return coord

def second_coord_change_for_bb(coord: int, size: int, image_size: int):
    """
    Method change coordinate from second pair of coordinates of rectangle on a random bigger values.

    :param coord - coordinate
    :param size - size of target box
    :param image_size - size of image in this demention
    :return coord
    """
    if coord + size // DIVIDER < image_size:
        coord += randint(0, size // DIVIDER)
    else:
        if image_size - coord > 0:
            coord += randint(0, image_size - coord)
    return coord
