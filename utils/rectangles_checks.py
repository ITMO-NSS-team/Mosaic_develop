



def line_intersect(first_line: list, second_line: list) -> bool:
    """
    This method check intersection of two lines

    :param first_line - first line
    :param second_line - second line

    :return bool

    """

    d = (second_line[3] - second_line[1]) * (first_line[2] - first_line[0]) \
         - (second_line[2] - second_line[0]) * (first_line[3] - first_line[1])
    if d:
        u_a = ((second_line[2] - second_line[0]) * (first_line[1] - second_line[1]) - \
             (second_line[3] - second_line[1]) * (first_line[0] - second_line[0])) / d
        u_b = ((first_line[2] - first_line[0]) * (first_line[1] - second_line[1]) - \
             (first_line[3] - first_line[1]) * (first_line[0] - second_line[0])) / d
    else:
        return False

    return (0 <= u_a <= 1 and 0 <= u_b <= 1)


def point_intersection(rect: list, x: int, y: int) -> bool:
    """
    This method check intersection of point and rectangle

    :param rect - first rectangle
    :param x - x coordinate of point
    :param y - y coordinate of point

    :return bool
    """
    return rect[0] <= x <= rect[2] and rect[1] <= y <= rect[3]

def rectangles_intersection(rectangle_1: list, rectangle_2: list) -> bool:
    intersect = False
    for i in range(0, 3, 2):
        if point_intersection(rectangle_1, rectangle_2[i], rectangle_2[i+1]):
            intersect = True
    for i in range(0, 3, 2):
        if point_intersection(rectangle_2, rectangle_1[i], rectangle_1[i+1]):
            intersect = True
    return intersect
    
def rectangle_correction(bbox: list, intersected_rectangle: list) -> list:
    bbox[0]
    if bbox[0] < intersected_rectangle[2]:
        bbox[0] = intersected_rectangle[2]
    elif bbox[2] > intersected_rectangle[0]:
        bbox[2] = intersected_rectangle[0]

    if bbox[1] < intersected_rectangle[3]:
        bbox[1] = intersected_rectangle[3]
    elif bbox[3] > intersected_rectangle[1]:
        bbox[3] = intersected_rectangle[1]
    return bbox