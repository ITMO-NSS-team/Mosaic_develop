from random import randint
from os.path import join
from typing import Tuple
from PIL import Image
import numpy as np

from utils.coord_utils import first_coord_change_for_bb, second_coord_change_for_bb
from utils.rectangles_checks import rectangles_intersection, multiply, \
    rectangle_correction_with_objects
from utils.convertors import from_rec_to_yolo, from_yolo_to_rec
from Constants.mosaic_settings import ATTEMPTS_FOR_GET_IMAGE_WITH_OBJECT

class DataPair:
    """
    Class-container for data pairs(image-annotation), that contains all information about
    images and txt-annotations.

    """
    image_folder: str
    text_folder: str

    img_width: int
    img_height: int

    image_name: str
    txt_name: str

    yolo_objects_list: list
    rec_objects_list: list

    object_number: int
    objects_classes: list
    
    def __init__(self, image_folder: str,
                 image_name: str, objects: list, classes: list) -> None:
        """
        Constructor
        :param image_folder - image folder
        :param image_name - name of image file
        :param objects - list of bounding boxes
        :param classes - likst of classes of objects
        """
        self.image_folder: str = image_folder
        self.image_name: str = image_name
        image = Image.open(join(self.image_folder, self.image_name))
        self.img_width, self.img_height = image.size
        self.objects_classes: list = classes.copy()
        self.object_number: int = len(self.objects_classes)

        # Check for format of bounding boxes
        if type(objects[0][0]) is int:
            # If it's just a rectangle
            self.rec_objects_list = objects.copy()
            self.yolo_objects_list = []
            for line in self.rec_objects_list:
                self.yolo_objects_list.append(from_rec_to_yolo(line,
                    self.img_width, self.img_height))
        elif type(objects[0][0]) is np.float64:
            # if it's in percentage
            self.rec_objects_list = []
            self.yolo_objects_list = objects.copy()
            for line in self.yolo_objects_list:
                self.rec_objects_list.append(from_yolo_to_rec(line, self.img_width, 
                self.img_height))
        elif  type(objects[0][0]) is np.int64:
            # If it's just a rectangle
            self.rec_objects_list = objects.copy()
            self.yolo_objects_list = []
            for line in self.rec_objects_list:
                self.yolo_objects_list.append(from_rec_to_yolo(line,
                    self.img_width, self.img_height))
        else:
            print ("ERROR! Annotation format error!")
            return 0

    def get_image(self) -> Image:
        """
        Returns image by path from class
        """
        return Image.open(join(self.image_folder, self.image_name))

    def get_image_piece_with_object(self, width: int, height: int, 
        min_multiplier: float, max_multiplier: float) -> Tuple[bool, list, list, list]:
        """
        This method returns image part with one or several 
        objects and four coordinates of this piece

        :param width
        :param height
        :param min_multiplier - min object multiplier
        :param max_multiplier - max object multiplier
        
        :return Image - returns Image or False
        :return out_rec_list - coordinates of image part
        :return out_pic_rect - coordinates of object
        :return classes_list - list of objects classes
        """
        out_rec_list_resized = []
        classes_list = []
        out_rec_list = []
        out_pic_rect = []
        if self.object_number == 0 or (30 >= width > 0) or (30 >= height > 0):
            return False, out_rec_list, out_pic_rect, classes_list
        else:
            stop: bool = False
            for _ in range(ATTEMPTS_FOR_GET_IMAGE_WITH_OBJECT):
                first_man_number = randint(0, len(self.rec_objects_list) - 1)
                out_x1: int = self.rec_objects_list[first_man_number][0]
                out_y1: int = self.rec_objects_list[first_man_number][1]
                out_x2: int = self.rec_objects_list[first_man_number][2]
                out_y2: int = self.rec_objects_list[first_man_number][3]
                objects_in_cropped_images = [first_man_number]
                out_x1 = first_coord_change_for_bb(out_x1, width)
                out_y1 = first_coord_change_for_bb(out_y1, height)
                out_x2 = second_coord_change_for_bb(out_x2, width, self.img_width)
                out_y2 = second_coord_change_for_bb(out_y2, height, self.img_height)
                stop = True
                for i in range(len(self.rec_objects_list)):
                    if rectangles_intersection([out_x1, out_y1, out_x2, out_y2], 
                                                    self.rec_objects_list[i]) \
                                                    and not (i in objects_in_cropped_images):
                        stop = False
                        out_x1, out_y1, out_x2, out_y2 = rectangle_correction_with_objects([out_x1, out_y1, out_x2, out_y2], self.rec_objects_list[i])
                        objects_in_cropped_images.append(i)
                if stop:
                    break

            out_rec_list: list = []
            for number in objects_in_cropped_images:
                out_rec_list.append([self.rec_objects_list[number][0] - out_x1,
                                     self.rec_objects_list[number][1] - out_y1,
                                     self.rec_objects_list[number][2] - out_x1,
                                     self.rec_objects_list[number][3] - out_y1])
                classes_list.append(self.objects_classes[number])
            out_pic_rect = [out_x1, out_y1, out_x2, out_y2]
            # Resizing!
            if not (width == 0 or height == 0):
                new_width: int= out_x2 - out_x1
                new_height: int = out_y2 - out_y1
                multiplier_width: float = width / new_width
                multiplier_height: float = height / new_height
                img = self.get_image().crop((out_x1, out_y1, out_x2, out_y2))
                if multiplier_width < multiplier_height:
                    if not min_multiplier < multiplier_width < max_multiplier:
                        return False, out_rec_list, out_pic_rect, classes_list
                    else:
                        for line in out_rec_list:
                            out_rec_list_resized.append(multiply(line, multiplier_width))
                        new_image = img.resize((int(new_width * multiplier_width), int(new_height * multiplier_width)))
                else:
                    if not min_multiplier < multiplier_height < max_multiplier:
                        return False, out_rec_list, out_pic_rect, classes_list
                    else:
                        for line in out_rec_list:
                            out_rec_list_resized.append(multiply(line, multiplier_height))
                        new_image = img.resize((int(new_width * multiplier_height), int(new_height * multiplier_height)))
                return new_image, out_rec_list_resized, out_pic_rect, classes_list
            else:
                return self.get_image().crop((out_x1, out_y1, out_x2, out_y2)), out_rec_list, out_pic_rect, classes_list