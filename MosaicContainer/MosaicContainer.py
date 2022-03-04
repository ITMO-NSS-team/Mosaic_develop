from pickle import FALSE
from random import randint
from os.path import join
from PIL import Image
import logging
from utils.rectangles_checks import point_intersection, rectangles_intersection
from utils.convertors import from_rec_to_yolo
from Constants.mosaic_settings import DELTA_Y, MAX_MULTIPLIER, MIN_MULTIPLIER, DELTA_X, DELTA_Y

class MosaicContainer:
    """
    Class-container for mosaic pair(image-annotation), that contains all information about
    image and txt-annotation of mosaic.
    """
    objects_number: int
    pieces_number: int
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
        self.mosaic_classes = []
        self.pieces_number = 0
        self.pair_list = pairs.copy()
        self.yolo_objects_list = []
        self.rec_objects_list = pairs[0].rec_objects_list.copy()
        self.rec_rec_list = []
        self.img_width = pairs[0].img_width
        self.img_height = pairs[0].img_height
        self.main_image = pairs[0].get_image()
        self.image_folder = arg_img_folder
        self.txt_folder = arg_txt_folder
        self.objects_number = pairs[0].object_number
        self.filename = filename
        for i in range(0, len(self.pair_list) - 1):
            if self.pair_list[i].object_number != len(self.pair_list[i].rec_objects_list):
                self.pair_list[i].object_number = len(self.pair_list[i].rec_objects_list)

        if self.objects_number == 1:
            self.mosaic_classes.append(pairs[0].objects_classes[0])
            self.yolo_objects_list.append(from_rec_to_yolo(self.rec_objects_list[0], self.img_width, self.img_height))
            self.get_small_area(self.rec_objects_list[0], DELTA_X, DELTA_Y)
        elif self.objects_number > 1:
            for i in range(len(pairs[0].objects_classes)):
                self.mosaic_classes.append(pairs[0].objects_classes[i])
                self.yolo_objects_list.append(from_rec_to_yolo(self.rec_objects_list[i], self.img_width, self.img_height))
                self.get_small_area(self.rec_objects_list[i], DELTA_X, DELTA_Y)
        else:
            self.objects_number = 0
            self.pieces_number = 0
        logging.info('Mosaic main image is ready')

    def make_mosaic(self) -> bool:
        """
        Creating mosaic from data inside the class

        :return bool
        """
        for i in range(0, len(self.pair_list) - 1):
            self.get_part_main_image()
        logging.info(f"Pieces in mosaic number: {self.pieces_number}")
        logging.info(f"Pieces in mosaic: {self.rec_rec_list}")
        self.insert_pics()
        if self.write_in_files():
            logging.info(f"Mosaic pair number {self.filename} was wrote successful!")
            return True
        else:
            logging.info(f"On mosaic pair number {self.filename} no people found! Or no mosaic was made.")
        return False
       

    def get_small_area(self, obj_coordinates, delta_w: int, delta_h: int) -> None:
        """
        Create random area around one single object on image

        :param obj_coordinates - object coordinates
        :param delta_w - width of area
        :param delta_h - height of area
        """
        def first_coord_change(coord: int, delta: int) -> int:
            if obj_coordinates[0] - delta_w >= 0:
                out_coord = coord - randint(0, delta)
            else:
                out_coord = coord - randint(0, coord)
            return out_coord

        def second_doord_change(coord: int, delta: int, size: int) -> int:
            if coord + delta <= size - 1:
                out_coord = coord + randint(0, delta)
            else:
                if size - coord <= 0:
                    out_coord = coord
                else:
                    out_coord = coord + randint(0, size - coord)
            return out_coord

        out_x1 = first_coord_change(obj_coordinates[0], delta_w)
        out_y1 = first_coord_change(obj_coordinates[1], delta_h)
        out_x2 = second_doord_change(obj_coordinates[2], delta_w, self.img_width)
        out_y2 = second_doord_change(obj_coordinates[3], delta_h, self.img_height)
        self.rec_rec_list.append([out_x1, out_y1, out_x2, out_y2])
        self.pieces_number += 1

    def write_in_files(self) -> bool:
        """
        Write mosaic pair in files

        """
        if self.objects_number != 0:
            if self.data_pairs_number != 0:
                self.main_image.save(join(self.image_folder, self.filename + ".jpg"))
                class_number = 0
                with open(join(self.txt_folder, self.filename + ".txt"), 'w') as f:
                    for item in self.yolo_objects_list:
                        f.write(f"{self.mosaic_classes[class_number]} ")
                        class_number += 1
                        for numb in item:
                            f.write(f"{numb} ")
                        f.write("\n")
                return True
        return False

    def get_part_main_image(self) -> None:
        """
        Get random empty part of image

        """
        areas = []
        if len(self.rec_rec_list) == 0:
            for n in range(15):
                out_x1 = randint(0, self.img_width - 1)
                out_y1 = randint(0, self.img_height - 1)
                if out_x1 == self.img_width - 1:
                    out_x2 = out_x1
                else:
                    out_x2 = randint(out_x1, self.img_width - 1)
                if out_y1 == self.img_height - 1:
                    out_y2 = out_y1
                else:
                    out_y2 = randint(out_y1, self.img_height - 1)
                areas.append([out_x1, out_y1, out_x2, out_y2])
            max_number = 0
            max_area = (areas[0][2] - areas[0][0]) * (areas[0][3] - areas[0][1])
            for i in range(len(areas)):
                if max_area < (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1]):
                    max_area = (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1])
                    max_number = i
            out_x1 = areas[max_number][0]
            out_y1 = areas[max_number][1]
            out_x2 = areas[max_number][2]
            out_y2 = areas[max_number][3]
            self.rec_rec_list.append([out_x1, out_y1, out_x2, out_y2])
            self.pieces_number += 1
        else:
            for n in range(15):
                x, y = 0, 0
                stop = False
                while not stop:
                    x = randint(1, self.img_width - 1)
                    y = randint(1, self.img_height - 1)
                    stop = True
                    for line in self.rec_rec_list:
                        if point_intersection(line, x, y):
                            stop = False

                out_x1 = x - randint(0, x)
                out_y1 = y - randint(0, y)
                out_x2 = randint(x, self.img_width - 1)
                out_y2 = randint(y, self.img_height - 1)
                is_good_area = False

                for i in range(len(self.rec_rec_list)):
                    for line in self.rec_rec_list:
                        if rectangles_intersection([out_x1, out_y1, out_x2, out_y2],
                                                   line):
                            if out_x1 < line[0] and out_y1 > line[1]:
                                if line[0] - 1 >= 0:
                                    out_x2 = line[0] - 1
                                else:
                                    out_x2 = line[0]
                            if out_x1 > line[0] and out_y1 < line[1]:
                                if line[1] - 1 >= 0:
                                    out_y2 = line[1] - 1
                                else:
                                    out_y2 = line[1]
                            if out_x2 > line[2] and out_y2 < line[3]:
                                if line[2] + 1 <= self.img_width:
                                    out_x1 = line[2] + 1
                                else:
                                    out_x1 = line[2]

                            if out_x2 < line[2] and out_y2 > line[3]:
                                if line[3] + 1 <= self.img_height:
                                    out_y1 = line[3] + 1
                                else:
                                    out_y1 = line[3]
                            # if up point is higher 
                            if out_x1 < line[0]:
                                if line[0] - 1 >= 0:
                                    out_x2 = line[0] - 1
                                else:
                                    out_x2 = line[0]
                            # if up point is left
                            if out_y1 < line[1]:
                                if line[1] - 1 >= 0:
                                    out_y2 = line[1] - 1
                                else:
                                    out_y2 = line[1]
                            # if lower point is lower    
                            if out_x2 > line[2]:
                                if line[2] + 1 <= self.img_width:
                                    out_x1 = line[2] + 1
                                else:
                                    out_x1 = line[2]
                            # if lower point is right  
                            if out_y2 > line[3]:
                                if line[3] + 1 <= self.img_height:
                                    out_y1 = line[3] + 1
                                else:
                                    out_y1 = line[3]

                            if rectangles_intersection([out_x1, out_y1, out_x2, out_y2],
                                                       line):
                                is_good_area = False
                                break
                            else:
                                is_good_area = True
                if is_good_area:
                    areas.append([out_x1, out_y1, out_x2, out_y2])
            if not len(areas) == 0:
                max_number = 0
                max_area = (areas[0][2] - areas[0][0]) * (areas[0][3] - areas[0][1])
                for i in range(len(areas)):
                    if max_area < (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1]):
                        max_area = (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1])
                        max_number = i
                out_x1 = areas[max_number][0]
                out_y1 = areas[max_number][1]
                out_x2 = areas[max_number][2]
                out_y2 = areas[max_number][3]
                if out_x2 - out_x1 > 1 and out_y2 - out_y1 > 1:
                    self.rec_rec_list.append([out_x1, out_y1, out_x2, out_y2])
                    self.pieces_number += 1

    def insert_pics(self) -> None:
        """
        Insert random parts with objects from pair images into empty parts of Main Image

        """
        for i in range(0, len(self.rec_rec_list)):
            width = self.rec_rec_list[i][2] - self.rec_rec_list[i][0]
            height = self.rec_rec_list[i][3] - self.rec_rec_list[i][1]
            for n in range(20):
                img, piece_of_objects_list, _, classes = self.pair_list[i].get_image_piece_with_object(width, height,
                                                                                                       self.min_object_multiplier,
                                                                                                       self.max_object_multiplier)
                if img:    
                    break
            if img:
                self.data_pairs_number += 1
                logging.info(f"Image in piece number {i} contains following objects: {piece_of_objects_list}")
                class_numb = 0
                for line in piece_of_objects_list:
                    self.mosaic_classes.append(classes[class_numb])
                    class_numb += 1
                    new_line = [line[0] + self.rec_rec_list[i][0], line[1] + self.rec_rec_list[i][1],
                                line[2] + self.rec_rec_list[i][0], line[3] + self.rec_rec_list[i][1]]
                    self.rec_objects_list.append(new_line)
                    self.yolo_objects_list.append(from_rec_to_yolo(new_line, self.img_width, self.img_height))
                self.main_image.paste(img, (self.rec_rec_list[i][0], self.rec_rec_list[i][1]))
