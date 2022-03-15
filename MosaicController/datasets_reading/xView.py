import json
import numpy as np
from tqdm import tqdm
from os.path import join, isfile
from PIL import Image

from DataPair.DataPair import DataPair
from Constants.start_settings import LOAD_COLOUR


def _is_more_than_zero(box: list) -> bool:
    """
    Method-checker for boxes. Checks if all elements in boxes are >0
    :param box - [x1, y1, x2, y2]
    :return True if all elements are > 0 and False otherwise
    """
    out = True
    for item in box:
        if item <= 0:
            out = False
    return out

def _is_in_bounds(box_list, width, height) -> bool:
    """
    Method-checker for boxes. Checks if all elements in boxes are x1 >= 0, y1 >= 0, x1 < width and y2 < height 
    and that list of boxes isn't empty
    :param box_list - [[x1, y1, x2, y2], [x1, y1, x2, y2],...]
    :param width, height - params of image
    :return True all of boxes are om bounds and list of boxes isn't empty, False otherwise
    """
    output = True
    for box in box_list:
        if not (box[0] >= 0 and box[1] >= 0 and box[2] < width and box[3] < height):
            output = False
    if len(box_list) == 0:
        output = False
    return output


def read_xView(images_path: str, json_path: str) -> list:
    """
    This method reads images and annotations in xView format and returns list of pairs

    :param images_path - path to images folder
    :param json_path - path to annotations file

    :return pair_list - list of data pairs
    """
    pair_list = []
    with open(json_path) as f:
        data = json.load(f)
    objects = []
    image = ""
    classes = []
    for i in tqdm(range(len(data['features'])), colour=LOAD_COLOUR):
        if data['features'][i]['properties']['bounds_imcoords'] != []:
            image_name = data['features'][i]['properties']['image_id']
            object_bb = np.array([int(num) for num in data['features'][i]['properties']['bounds_imcoords'].split(",")])
            class_of_object = data['features'][i]['properties']['type_id']
            if object_bb.shape != (4,):
                print("Issues at %d!" % i)
                return False, pair_list
            if image == "":
                image = image_name
                objects = []
                classes = []
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image == image_name:
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image != image_name:
                if (isfile(join(images_path, image))):
                    img = Image.open(join(images_path, image)).convert("RGB")
                    img_width, img_height = img.size
                    if _is_in_bounds(objects, img_width, img_height):
                        pair_list.append(DataPair(images_path, image, objects, classes))
                image = image_name
                objects = []
                classes = []
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
    img = Image.open(join(images_path, image)).convert("RGB")
    img_width, img_height = img.size
    if _is_in_bounds(objects, img_width, img_height):
        pair_list.append(DataPair(images_path, image, objects, classes))
    return True, pair_list