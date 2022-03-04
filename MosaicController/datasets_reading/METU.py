import json
import numpy as np
from tqdm import tqdm
from os.path import join, isfile
import sys
sys.path.append ("/home/nikita/Desktop/Mosaic_develop")
from DataPair.DataPair import DataPair

def _is_more_than_zero(box: list) -> bool:
    out = True
    for item in box:
        if item < 0:
            out = False
    return out

def _search_filename_by_imageID(data, imageID: int) -> str:
    for i in range(len(data['images'])):
        if data['images'][i]['id'] == imageID:
            return data['images'][i]['file_name']


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
            if object_bb.shape[0] != 4:
                print("Issues at %d!" % i)
                return False, pair_list
            if image == "":
                image = image_id
                objects = []
                classes = []
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image == image_id:
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
            elif image != image_id:
                image_name = _search_filename_by_imageID(data, image)
                if (isfile(join(images_path, image_name))):
                    pair_list.append(DataPair(images_path, image_name, objects, classes))
                image = image_id
                objects = []
                classes = []
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
                
        image_name = _search_filename_by_imageID(data, image)
        if (isfile(join(images_path, image_name))):
            pair_list.append(DataPair(images_path, image_name, objects, classes))
    return True, pair_list
