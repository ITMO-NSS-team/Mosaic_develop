import json
import numpy as np
from tqdm import tqdm
import os
from os.path import splitext


def read_yolov4(img_path: str, txt_path: str):
    image_list = next(os.walk(img_path))[2]
    image_list.sort()
    txt_list = next(os.walk(txt_path))[2]
    txt_list.sort()
    if len(image_list) == len(txt_list):
        pair_count = len(txt_list)
        is_all_files_paired = True
        for i in tqdm(range(pair_count), colour="red"):
            img_pathname, img_extension = splitext(image_list[i])
            txt_pathname, txt_extension = splitext(txt_list[i])
            if not (img_pathname == txt_pathname and img_extension in self.img_ext and txt_extension == self.txt_ext):
                print(f"ERROR! Pair {i}: img {self.image_list[i]} - txt {aself.txt_list[i]}")
                is_all_files_paired = False
        if is_all_files_paired:
            print(f"All images have a respective pair of text files!")
            print(f"Pair count is {self.pair_count}")
            for i in tqdm(range(self.pair_count), colour="blue"):
                self.pair_list.append(DataPair(self.input_image_folder, self.input_text_folder, self.image_list[i],
                                                self.txt_list[i]))
        else:
            print(f"ERROR! Not all images have a respective pair of text files!")
    elif len(self.image_list) > len(self.txt_list):
        print(f"ERROR! Not all images have a respective pair of text files!")
        print(f"There is {len(self.image_list) - len(self.txt_list)} images without pairs")
    else:
        print(f"ERROR! Not all images have a respective pair of text files!")
        print(f"There is {len(self.txt_list) - len(self.image_list)} txt files without pairs")
