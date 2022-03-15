from pickle import FALSE
from random import randint
from os.path import join
from PIL import Image
import logging

import cv2
from utils.rectangles_checks import point_intersection, rectangles_intersection, rectangle_correction, is_not_degenerate
from utils.images_utils import get_space_on_empty_image
from utils.convertors import from_rec_to_yolo
from Constants.mosaic_settings import DELTA_Y, MAX_MULTIPLIER, MIN_MULTIPLIER, DELTA_X, DELTA_Y

class MosaicContainer:
    """
    Class-container for mosaic pair(image-annotation), that contains all information about
    image and txt-annotation of mosaic.
    """
    objects_number: int
    img_width: int
    img_height: int
    yolo_objects_list: list
    rec_objects_list: list
    rec_rec_list: list
    main_image: Image
    pair_list: list
    image_folder: str
    txt_folder: str
    filename: str
    pair_classes: list
    mosaic_classes: list
    data_pairs_number: int
    min_object_multiplier: int
    max_object_multiplier: int
    areas_list: list

    def __init__(self, pairs: list, arg_img_folder: str, arg_txt_folder: str, filename: str):
        """
        Constructor - takes in Data_pair type objects list 
        First object contain 1 or 0 people

        :param pairs - list of pairs
        :param arg_img_folder - save folder for image
        :param arg_txt_folder - save folder for annotation
        :param filename - name of image and annotation file

        """
        self.data_pairs_number = 0
        self.min_object_multiplier = MIN_MULTIPLIER
        self.max_object_multiplier = MAX_MULTIPLIER
        self.pair_classes = []
        self.mosaic_classes = pairs[0].objects_classes.copy()
        self.pair_list = pairs.copy()
        self.yolo_objects_list = pairs[0].yolo_objects_list.copy()
        self.rec_objects_list = pairs[0].rec_objects_list.copy()

        # list for small areas aroun objects to improve quality 
        self.rec_rec_list = []
        # list of inserted areas
        self.areas_list = []
        self.img_width = pairs[0].img_width
        self.img_height = pairs[0].img_height
        self.main_image = pairs[0].get_image()
        self.image_folder = arg_img_folder
        self.txt_folder = arg_txt_folder
        self.objects_number = pairs[0].object_number
        self.filename = filename
        self.get_small_area(DELTA_X, DELTA_Y)
        logging.info('Mosaic main image is ready')

    def make_mosaic(self) -> bool:
        """
        Creating mosaic from data inside the class

        :return bool
        """
        for i in range(0, len(self.pair_list) - 1):
            self.get_part_main_image()
        logging.info(f"Pieces in mosaic: {len(self.rec_rec_list)}")
        self.insert_pics()
        if self.write_in_files():
            logging.info(f"Mosaic pair number {self.filename} was wrote successful!")
            return True
        else:
            logging.info(f"On mosaic pair number {self.filename} no people found! Or no mosaic was made.")
        return False
       

    def get_small_area(self, delta_w: int, delta_h: int) -> None:
        """
        Create random area around one single object on image

        :param obj_coordinates - object coordinates
        :param delta_w - width of area
        :param delta_h - height of area
        """
        def first_coord_change(coord: int, delta: int) -> int:
            if coord - delta >= 0:
                out_coord = coord - randint(0, delta)
            else:
                out_coord = coord - randint(0, coord)
            return out_coord

        def second_coord_change(coord: int, delta: int, size: int) -> int:
            if coord + delta <= size - 1:
                out_coord = coord + randint(0, delta)
            else:
                if size - coord <= 0:
                    out_coord = coord
                else:
                    out_coord = coord + randint(0, size - coord)
            return out_coord
        for bbox in self.rec_objects_list:
            out_x1 = first_coord_change(bbox[0], delta_w)
            out_y1 = first_coord_change(bbox[1], delta_h)
            out_x2 = second_coord_change(bbox[2], delta_w, self.img_width)
            out_y2 = second_coord_change(bbox[3], delta_h, self.img_height)
            self.rec_rec_list.append([out_x1, out_y1, out_x2, out_y2])

    def write_in_files(self) -> bool:
        """
        Write mosaic pair in files

        """
        if self.objects_number != 0:
            if self.data_pairs_number != 0:
                self.main_image.save(join(self.image_folder, self.filename + ".jpg"))
                with open(join(self.txt_folder, self.filename + ".txt"), 'w') as f:
                    for i in range(len(self.yolo_objects_list)):
                        f.write(f"{self.mosaic_classes[i]} ")
                        for numb in self.yolo_objects_list[i]:
                            f.write(f"{numb} ")
                        f.write("\n")
                return True
        return False

    def get_part_main_image(self):
        """
        This method returns image part without any objects - four 
        coordinates of this piece
        
        :param width
        :param height

        :return Image - returns Image or False
        :return out_list - coordinates of image part
        """
        out_list: list = []
        if len(self.rec_rec_list) == 0:
            out_list = get_space_on_empty_image(self.img_width, self.img_height)
            self.areas_list.append(out_list)
        else:
            main_stop = False
            while not main_stop:
                areas = []
                x: int = 0
                y: int = 0
                for n in range(15):
                    stop: bool = False
                    while not stop:
                        x = randint(0, self.img_width - 1)
                        y = randint(0, self.img_height - 1)
                        stop = True
                        for bbox in self.rec_rec_list:
                            if point_intersection(bbox, x, y):
                                stop = False
                        for bbox in self.areas_list:
                            if point_intersection(bbox, x, y):
                                stop = False

                    out_x1: int = x - randint(0, x)
                    out_y1: int = y - randint(0, y)
                    out_x2: int = randint(x, self.img_width - 1)
                    out_y2: int = randint(y, self.img_height - 1)
                    bbox = [out_x1, out_y1, out_x2, out_y2]
                    is_good_area: bool = True
                    for existing_bbox in self.rec_rec_list:
                        if rectangles_intersection(bbox, existing_bbox):
                            bbox = rectangle_correction(bbox, existing_bbox)
                    for existing_bbox in self.rec_rec_list:
                        if rectangles_intersection(bbox, existing_bbox):
                            if rectangles_intersection(bbox, existing_bbox):
                                is_good_area = False
                                break
                    for existing_bbox in self.areas_list:
                        if rectangles_intersection(bbox, existing_bbox):
                            bbox = rectangle_correction(bbox, existing_bbox)
                    for existing_bbox in self.areas_list:
                        if rectangles_intersection(bbox, existing_bbox):
                            if rectangles_intersection(bbox, existing_bbox):
                                is_good_area = False
                                break
                    if is_not_degenerate(bbox) and is_good_area:
                        areas.append(bbox)
                if len(areas):
                    max_number: int = 0
                    max_area: list = (areas[0][2] - areas[0][0]) * (areas[0][3] - areas[0][1])
                    for i in range(len(areas)):
                        if max_area < (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1]):
                            max_area = (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1])
                            max_number: int = i
                    self.areas_list.append(areas[max_number])
                main_stop = True

    def insert_pics(self) -> None:
        """
        Insert random parts with objects from pair images into empty parts of Main Image

        """
        for i in range(len(self.areas_list)):
            if i < len(self.areas_list):
                rectangle = self.areas_list.pop(i)
                width: int = rectangle[2] - rectangle[0]
                height: int = rectangle[3] - rectangle[1]
                for n in range(20):
                    number = randint(1, len(self.pair_list)-1)
                    img, piece_of_objects_list, _, classes = self.pair_list[number].get_image_piece_with_object(width, height,
                                                                                                        self.min_object_multiplier,
                                                                                                        self.max_object_multiplier)
                    if img:    
                        break
                if img:
                    self.data_pairs_number += 1
                    logging.info(f"Image in piece number {i} contains following objects: {piece_of_objects_list}")
                    for i in range(len(piece_of_objects_list)):
                        self.mosaic_classes.append(classes[i])
                        new_line = [piece_of_objects_list[i][0] + rectangle[0], piece_of_objects_list[i][1] + rectangle[1],
                                    piece_of_objects_list[i][2] + rectangle[0], piece_of_objects_list[i][3] + rectangle[1]]
                        self.rec_objects_list.append(new_line)
                        self.yolo_objects_list.append(from_rec_to_yolo(new_line, self.img_width, self.img_height))
                    self.main_image.paste(img, (rectangle[0], rectangle[1]))
                    
