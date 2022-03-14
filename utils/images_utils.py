from random import randint

def get_space_on_empty_image(img_width: int, img_height: int, 
                            width: int, height: int) -> list:
    """
    This method returns four coordinates of empty objects or False if image are too small
    
    :param img_width
    :param img_height
    :param width
    :param height

    :return out_list - coordinates of image part
    """
    if img_width == width:
            out_x1: int = 0
            out_x2: int = width
    elif img_width > width:
        out_x1: int = randint(0, int(img_width - width))
        out_x2: int = out_x1 + width
    else:
        return False
    if img_height == height:
        out_y1: int = 0
        out_y2: int = width
    elif img_height > height:
        out_y1: int = randint(0, int(img_height - height))
        out_y2: int = out_y1 + height
    else:
        return False
    return [out_x1, out_y1, out_x2, out_y2]