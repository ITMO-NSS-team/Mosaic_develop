



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
    
def rectangles_intersection_old(rectangle_1: list, rectangle_2: list) -> bool:
    """
    This method check intersection of two rectangles
    :param rectangle_1 - first rectangle
    :param rectangle_2 - second rectangle

    :return bool
    """
    rec1_x1, rec1_y1, rec1_x2, rec1_y2 = rectangle_1
    rec2_x1, rec2_y1, rec2_x2, rec2_y2 = rectangle_2

    x_y_match = (rec1_x1 < rec2_x2 < rec1_x2 or rec1_x1 < rec2_x1 < rec2_x2) and \
        (rec2_y2 > rec1_y1 > rec2_y2 or rec1_y1 < rec2_y1 < rec1_y2)



    in_match = rec1_x1 < rec2_x1 and rec1_y1 < rec2_y1 and rec1_x2 > rec2_x2 and rec1_y2 > rec2_y2

    # x1, y1
    # x1, y2
    # x2, y1
    # x2, vertical_line_match

    angle_match = ((rec1_x1 < rec2_x1 < rec1_x2) and (rec1_y1 < rec2_y1 < rec1_y2)) or \
            ((rec1_x1 < rec2_x1 < rec1_x2) and (rec1_y1 < rec2_y2 < rec1_y2)) or \
            ((rec1_x1 < rec2_x2 < rec1_x2) and (rec1_y1 < rec2_y1 < rec1_y2)) or \
            ((rec1_x1 < rec2_x2 < rec1_x2) and (rec1_y1 < rec2_y2 < rec1_y2))


    out_match = (rec1_x1 < rec2_x1 and rec1_y1 > rec2_y1 and rec1_x2 > rec2_x2 and rec1_y2 < rec2_y2) or \
            (rec1_x1 > rec2_x1 and rec1_y1 < rec2_y1 and rec1_x2 > rec2_x2 and rec1_y2 > rec2_y2)

    point_match = False
    rect = [rec1_x1, rec1_y1, rec1_x2, rec1_y2]
    if point_intersection(rect, rec2_x1, rec2_y1):
        point_match = True
    if point_intersection(rect, rec2_x2, rec2_y2):
        point_match = True
    rect = [rec2_x1, rec2_y1, rec2_x2, rec2_y2]
    if point_intersection(rect, rec1_x1, rec1_y1):
        point_match = True
    if point_intersection(rect, rec1_x2, rec1_y2):
        point_match = True

    vertical_line_match = line_intersect([rec1_x1, rec1_y1, rec1_x1, rec1_y2], [rec2_x1, rec2_y1, rec2_x2, rec2_y1]) or \
            line_intersect([rec1_x1, rec1_y1, rec1_x1, rec1_y2], [rec2_x1, rec2_y2, rec2_x2, rec2_y2]) or \
            line_intersect([rec1_x2, rec1_y1, rec1_x2, rec1_y2], [rec2_x1, rec2_y1, rec2_x2, rec2_y1]) or \
            line_intersect([rec1_x2, rec1_y2, rec1_x1, rec1_y2], [rec2_x1, rec2_y2, rec2_x2, rec2_y2])

    horizontal_line_match = False
    horizontal_line_match = line_intersect([rec1_x1, rec1_y1, rec1_x2, rec1_y1], [rec2_x1, rec2_y1, rec2_x1, rec2_y2]) or \
            line_intersect([rec1_x1, rec1_y1, rec1_x2, rec1_y1], [rec2_x2, rec2_y1, rec2_x2, rec2_y2]) or \
            line_intersect([rec1_x1, rec1_y2, rec1_x2, rec1_y2], [rec2_x1, rec2_y1, rec2_x1, rec2_y2]) or \
            line_intersect([rec1_x1, rec1_y2, rec1_x2, rec1_y2], [rec2_x2, rec2_y1, rec2_x2, rec2_y2])

    return  x_y_match or in_match or angle_match or out_match or point_match or horizontal_line_match or vertical_line_match