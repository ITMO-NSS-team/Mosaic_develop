import json
from re import T
import numpy as np
from tqdm import tqdm
from os.path import join, isfile
from DataPair.DataPair import DataPair

def _is_more_than_zero(box: list) -> bool:
    out = True
    for item in box:
        if item < 0:
            out = False
    return out


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
    for i in tqdm(range(len(data['features']))):
        if data['features'][i]['properties']['bounds_imcoords'] != []:
            image_name = data['features'][i]['properties']['image_id']
            object_bb = np.array([int(num) for num in data['features'][i]['properties']['bounds_imcoords'].split(",")])
            class_of_object = data['features'][i]['properties']['type_id']
            if object_bb.shape[0] != 4:
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
                    pair_list.append(DataPair(images_path, image, objects, classes))
                image = image_name
                objects = []
                classes = []
                if _is_more_than_zero(object_bb):
                    objects.append(object_bb)
                    classes.append(class_of_object)
    pair_list.append(DataPair(images_path, image, objects, classes))
    return True, pair_list