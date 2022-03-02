import json
import numpy as np
from tqdm import tqdm
import os

def read_data_from_xView(path: str) -> list:
    with open(path) as f:
        data = json.load(f)
    pairs = []
    image = ""
    bb_list = []
    for i in tqdm(range(len(data['features']))):
        if data['features'][i]['properties']['bounds_imcoords'] != []:
            b_id = data['features'][i]['properties']['image_id']
            val = np.array([int(num) for num in data['features'][i]['properties']['bounds_imcoords'].split(",")])
            class_of_object = data['features'][i]['properties']['type_id']
            if val.shape[0] != 4:
                print("Issues at %d!" % i)
                return 0
            if image == "":
                image = b_id
                bb_list = []
                bb_list.append((class_of_object, val))
            elif image == b_id:
                bb_list.append((class_of_object, val))
            elif image != b_id:
                pairs.append((image, bb_list))
                image = b_id
                bb_list = []
                bb_list.append((class_of_object, val))
    pairs.append((image, bb_list))
    return pairs