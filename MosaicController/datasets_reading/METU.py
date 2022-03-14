import json
import numpy as np
from tqdm import tqdm
from os.path import join, isfile
import sys
sys.path.append ("/home/balin/Desktop/Mosaic_develop")
from DataPair.DataPair import DataPair
from PIL import Image

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

def _search_filename_by_imageID(data: dict, imageID: int) -> str:
    """
    Method-searcher for filenames in json annotation by imageID
    :param data - data read from json
    :param imageID - ide of image

    :return filename
    """
    for i in range(len(data['images'])):
        if data['images'][i]['id'] == imageID:
            return data['images'][i]['file_name']


def _is_not_degenerate(box: list) -> bool:
    """
    Method-checker for boxes. Checks if all elements in boxes are x1 < x2 and y1 < y2(not degenerate)
    :param box - [x1, y1, x2, y2]
    :return True if box isn't degenerate and False otherwise
    """
    if box[0] >= box[2] or box[1] >= box[3]:
        return False
    return True

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

def read_METU(images_path: str, json_path: str) -> list:
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
    for i in tqdm(range(len(data['annotations']))):
        if data['annotations'][i]['bbox'] != []:
            image_id = data['annotations'][i]['image_id']
            object_bb_1 = np.array([int(num) for num in data['annotations'][i]['bbox']])
            object_bb = np.array(([object_bb_1[0], object_bb_1[1], object_bb_1[0]+object_bb_1[2], object_bb_1[1]+object_bb_1[3]]))
            class_of_object = data['annotations'][i]['category_id']
            if object_bb.shape != (4,):
                print("Issues at %d!" % i)
                return False, pair_list
            if image == "":
                image = image_id
                objects = []
                classes = []
                if _is_more_than_zero(object_bb) and _is_not_degenerate(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image == image_id:
                if _is_more_than_zero(object_bb) and _is_not_degenerate(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image != image_id:
                image_name = _search_filename_by_imageID(data, image)
                if isfile(join(images_path, image_name)):
                    img = Image.open(join(images_path, image_name)).convert("RGB")
                    img_width, img_height = img.size
                    if _is_in_bounds(objects, img_width, img_height):
                        pair_list.append(DataPair(images_path, image_name, objects, classes))
                image = image_id
                objects = []
                classes = []
                if _is_more_than_zero(object_bb) and _is_not_degenerate(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
                
        image_name = _search_filename_by_imageID(data, image)
        if isfile(join(images_path, image_name)):
            img = Image.open(join(images_path, image_name)).convert("RGB")
            img_width, img_height = img.size
            if _is_in_bounds(objects, img_width, img_height):
                pair_list.append(DataPair(images_path, image_name, objects, classes))
    return True, pair_list
