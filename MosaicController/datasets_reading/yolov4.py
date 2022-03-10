from tqdm import tqdm
import os
from os.path import splitext
from DataPair.DataPair import DataPair

img_ext = [".jpg", ".png", ".JPG", ".PNG"]
txt_ext = [".txt", ".TXT"]

def read_yolov4(images_path: str, annotations_path: str) -> list:
    """
    This method reads images and annotations in YOLOv4 format and returns list of pairs

    :param images_path - path to images folder
    :param annotations_path - path to annotations folder

    :return pair_list - list of data pairs
    """
    pair_list = []
    image_list = next(os.walk(images_path))[2]
    image_list.sort()
    txt_list = next(os.walk(annotations_path))[2]
    txt_list.sort()
    if len(image_list) == len(txt_list):
        pair_count = len(txt_list)
        is_all_files_paired = True
        for i in tqdm(range(pair_count), colour="red"):
            img_pathname, img_extension = splitext(image_list[i])
            txt_pathname, txt_extension = splitext(txt_list[i])
            if not (img_pathname == txt_pathname and img_extension in img_ext and txt_extension in txt_ext):
                print(f"ERROR! Pair {i}: img {image_list[i]} - txt {txt_list[i]}")
                is_all_files_paired = False
        if is_all_files_paired:
            print(f"All images have a respective pair of text files!")
            print(f"Pair count is {pair_count}")
            for i in tqdm(range(pair_count), colour="blue"):
                pair_list.append(DataPair(images_path, annotations_path, image_list[i],
                                                txt_list[i]))
        else:
            print(f"ERROR! Not all images have a respective pair of text files!")
            return False, pair_list
    elif len(image_list) > len(txt_list):
        print(f"ERROR! Not all images have a respective pair of text files!")
        print(f"There is {len(image_list) - len(txt_list)} images without pairs")
        return False, pair_list
    else:
        print(f"ERROR! Not all images have a respective pair of text files!")
        print(f"There is {len(txt_list) - len(image_list)} txt files without pairs")
        return False, pair_list
    return True, pair_list
