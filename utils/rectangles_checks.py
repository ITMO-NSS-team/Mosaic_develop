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
    return rect[0] < x < rect[2] and rect[1] < y < rect[3]

def rectangles_intersection(rectangle_1: list, rectangle_2: list) -> bool:
    """
    Method check is two rectangles intersect each other. Returns true if rectangles intersected. False otherwise.
    :param rectangle_1 - [x1, y1, x2, y2] - rectangle one
    :param rectangle_2 - [x1, y1, x2, y2] - rectangle two
    :return bool
    """
    intersect = False
    if point_intersection(rectangle_1, rectangle_2[0], rectangle_2[1]) or \
            point_intersection(rectangle_1, rectangle_2[0], rectangle_2[3]) or \
                point_intersection(rectangle_1, rectangle_2[2], rectangle_2[3]) or \
                    point_intersection(rectangle_1, rectangle_2[2], rectangle_2[1]):
        intersect = True
    if point_intersection(rectangle_2, rectangle_1[0], rectangle_1[1]) or \
            point_intersection(rectangle_2, rectangle_1[0], rectangle_1[3]) or \
                point_intersection(rectangle_2, rectangle_1[2], rectangle_1[3]) or \
                    point_intersection(rectangle_2, rectangle_1[2], rectangle_1[1]):
        intersect = True
    #first_rec
    lines_of_first_rec = []
    lines_of_first_rec.append([rectangle_1[0], rectangle_1[1], rectangle_1[0], rectangle_1[3]])
    lines_of_first_rec.append([rectangle_1[0], rectangle_1[3], rectangle_1[2], rectangle_1[3]])
    lines_of_first_rec.append([rectangle_1[2], rectangle_1[3], rectangle_1[2], rectangle_1[1]])
    lines_of_first_rec.append([rectangle_1[0], rectangle_1[1], rectangle_1[2], rectangle_1[1]])
    #second_rec
    lines_of_second_rec = []
    lines_of_second_rec.append([rectangle_2[0], rectangle_2[1], rectangle_2[0], rectangle_2[3]])
    lines_of_second_rec.append([rectangle_2[0], rectangle_2[3], rectangle_2[2], rectangle_2[3]])
    lines_of_second_rec.append([rectangle_2[2], rectangle_2[3], rectangle_2[2], rectangle_2[1]])
    lines_of_second_rec.append([rectangle_2[0], rectangle_2[1], rectangle_2[2], rectangle_2[1]])

    for line_of_rec1 in lines_of_first_rec:
        for line_of_rec2 in lines_of_second_rec:
            if line_intersect(line_of_rec1, line_of_rec2):
                intersect = True
    return intersect

def is_line_inside_rectangle(rectangle: list, line: list) -> bool:
    """
    Method check is line lies inside rectangle. Returns true if line are inside another. False otherwise.
    :param rectangle_1 - [x1, y1, x2, y2] - rectangle
    :param line - [x1, y1, x2, y2] - line
    :return bool
    """
    return point_intersection(rectangle, line[0], line[1]) and point_intersection(rectangle, line[2], line[3])

def is_any_line_of_rectangle1_inside_another_rectangle2(rectangle_1: list, rectangle_2: list) -> bool:
    """
    Method check is lines of rectangles lies inside each others. Returns true if one of lines of one rectangle are inside another. False otherwise.
    :param rectangle_1 - [x1, y1, x2, y2] - rectangle one
    :param rectangle_2 - [x1, y1, x2, y2] - rectangle two
    :return bool
    """
    return  is_line_inside_rectangle(rectangle_2, [rectangle_1[0], rectangle_1[1], rectangle_1[0], rectangle_1[3]]) or \
                is_line_inside_rectangle(rectangle_2, [rectangle_1[2], rectangle_1[1], rectangle_1[2], rectangle_1[3]]) or \
                    is_line_inside_rectangle(rectangle_2, [rectangle_1[0], rectangle_1[1], rectangle_1[2], rectangle_1[1]]) or \
                        is_line_inside_rectangle(rectangle_2, [rectangle_1[0], rectangle_1[3], rectangle_1[2], rectangle_1[3]])

def rectangle_correction(bbox: list, intersected_rectangle: list) -> list:
    """
    Method make bounding box smaller - to fully avoid intersected objects
    :param bbox - [x1, y1, x2, y2] - bounding boxe
    :param intersected_rectangle - [x1, y1, x2, y2] - objects
    :return bbox - [x1, y1, x2, y2]
    """
    if is_any_line_of_rectangle1_inside_another_rectangle2(bbox, intersected_rectangle):
        if is_line_inside_rectangle(intersected_rectangle, [bbox[0], bbox[1], bbox[0], bbox[3]]): 
            bbox[0] = intersected_rectangle[2]
        if is_line_inside_rectangle(intersected_rectangle, [bbox[2], bbox[1], bbox[2], bbox[3]]): 
            bbox[2] = intersected_rectangle[0]
        if is_line_inside_rectangle(intersected_rectangle, [bbox[0], bbox[1], bbox[2], bbox[1]]): 
            bbox[1] = intersected_rectangle[3]
        if is_line_inside_rectangle(intersected_rectangle, [bbox[0], bbox[3], bbox[2], bbox[3]]): 
            bbox[3] = intersected_rectangle[1]
    else:
        # x1, y1
        if point_intersection(intersected_rectangle, bbox[0], bbox[1]):
            bbox[0] = intersected_rectangle[2]
            bbox[1] = intersected_rectangle[3]
        # x2, y2
        if point_intersection(intersected_rectangle, bbox[2], bbox[3]):
            bbox[2] = intersected_rectangle[0]
            bbox[3] = intersected_rectangle[1]
        # x1, y2
        if point_intersection(intersected_rectangle, bbox[0], bbox[3]):
            bbox[0] = intersected_rectangle[1]
            bbox[3] = intersected_rectangle[2]
        # x2, y1
        if point_intersection(intersected_rectangle, bbox[2], bbox[1]):
            bbox[1] = intersected_rectangle[0]
            bbox[2] = intersected_rectangle[3]
    return bbox

def rectangle_correction_with_objects(bbox: list, intersected_rectangle: list) -> list:
    """
    Method make bounding box bigger - to fully cover object that was intersected by this bounding box
    :param bbox - [x1, y1, x2, y2] - bounding boxe
    :param intersected_rectangle - [x1, y1, x2, y2] - objects
    :return bbox - [x1, y1, x2, y2]
    """
    if bbox[0] > intersected_rectangle[0]:
        bbox[0] = intersected_rectangle[0]
    if bbox[1] > intersected_rectangle[1]:
        bbox[1] = intersected_rectangle[1]
    if bbox[2] < intersected_rectangle[2]:
        bbox[2] = intersected_rectangle[2]
    if bbox[3] < intersected_rectangle[3]:
        bbox[3] = intersected_rectangle[3]
    return bbox


def is_not_degenerate(box: list) -> bool:
    """
    Method-checker for boxes. Checks if all elements in boxes are x1 < x2 and y1 < y2(not degenerate)
    :param box - [x1, y1, x2, y2]
    :return True if box isn't degenerate and False otherwise
    """
    if box[0] >= box[2] or box[1] >= box[3]:
        return False
    return True

def multiply(bbox: list, multiplier: float) -> list:
    """
    Method-multiplier for bounding box
    :param bbox - [x1, y1, x2, y2]
    :param multiplier
    :return list
    """
    return [int(i * multiplier) for i in bbox]
