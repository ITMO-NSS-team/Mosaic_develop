from random import randint
from os.path import join
from typing import Tuple
from PIL import Image
import numpy as np

from utils.images_utils import get_space_on_empty_image
from utils.rectangles_checks import point_intersection, rectangles_intersection, \
    rectangle_correction
from utils.convertors import from_rec_to_yolo, from_yolo_to_rec

class DataPair:
    """
    Class-container for data pairs(image-annotation), that contains all information about
    images and txt-annotations.

    """
    image_folder: str
    text_folder: str
    image_name: str
    txt_name: str
    yolo_objects_list: list
    rec_objects_list: list
    img_width: int
    img_height: int
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
        self.image_folder = image_folder
        self.image_name = image_name
        image = Image.open(join(self.image_folder, self.image_name))
        self.img_width, self.img_height = image.size
        self.objects_classes = classes.copy()
        self.object_number = len(self.objects_classes)

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

    def get_free_space_on_image(self, width: int, height: int) -> Tuple[bool, list]:
        """
        This method returns image part without any objects and four 
        coordinates of this piece
        
        :param width
        :param height

        :return Image - returns Image or False
        :return out_list - coordinates of image part
        """
        out_list: list = []
        if self.object_number == 0:
            out_list = get_space_on_empty_image(self.img_width, 
            self.img_height, width, height)
            if out_list:
                return self.get_image().crop((
                     out_list[0], out_list[1], out_list[2], out_list[3])), \
                      out_list
            else:
                return False, []
        else:
            areas = []
            x: int = 0
            y: int = 0
            for n in range(15):
                stop: bool = False
                while not stop:
                    x = randint(0, self.img_width - 1)
                    y = randint(0, self.img_height - 1)
                    stop = True
                    for line in self.rec_objects_list:
                        if point_intersection([line[0], line[1], line[2], 
                        line[3]], x, y):
                            stop = False

                out_x1: int = x - randint(0, x)
                out_y1: int = y - randint(0, y)
                out_x2: int = randint(x, self.img_width - 1)
                out_y2: int = randint(y, self.img_height - 1)
                bbox = [out_x1, out_y1, out_x2, out_y2]

                for i in range(len(self.rec_objects_list)):
                    if rectangles_intersection(bbox, 
                                                [self.rec_objects_list[i][0],
                                                self.rec_objects_list[i][1],
                                                self.rec_objects_list[i][2],
                                                self.rec_objects_list[i][3]]):
                        bbox = rectangle_correction(bbox, 
                                                self.rec_objects_list[i], self.img_width, self.img_height).copy()
                areas.append(bbox)

            max_number: int = 0
            max_area: list = (areas[0][2] - areas[0][0]) * (areas[0][3] - areas[0][1])
            for i in range(len(areas)):
                if max_area < (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1]):
                    max_area = (areas[i][2] - areas[i][0]) * (areas[i][3] - areas[i][1])
                    max_number: int = i
            out_x1: int = areas[max_number][0]
            out_y1: int = areas[max_number][1]
            out_x2: int = areas[max_number][2]
            out_y2: int = areas[max_number][3]

            out_list: list = [out_x1, out_y1, out_x2, out_y2]
            if out_x2 - out_x1 > 1 and out_y2 - out_y1 > 1:
                if out_x2 - out_x1 >= width and out_y2 - out_y1 >= height:
                    return self.get_image().crop((out_x1, out_y1, out_x1 + width, out_y1 + height)), out_list
                else:
                    new_width = out_x2 - out_x1
                    new_height = out_y2 - out_y1
                    multiplier_width = 1
                    multiplier_height = 1
                    if width > new_width:
                        multiplier_width = width / new_width
                    if height > new_height:
                        multiplier_height = height / new_height

                    if multiplier_width > multiplier_height:
                        img = self.get_image().crop((out_x1, out_y1, 
                        out_x2, out_y2))
                        new_image = img.resize((int(new_width * multiplier_width), int(new_height * multiplier_width)))
                    else:
                        img = self.get_image().crop((out_x1, out_y1, out_x2, out_y2))
                        new_image = img.resize(
                            (int(new_width * multiplier_height), int(new_height * multiplier_height)))
                    return new_image.crop((0, 0, width, height)), out_list
            return False, out_list

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
        out_list_1 = []
        classes_list = []
        out_rec_list = []
        out_pic_rect = []
        if self.object_number == 0 or (30 >= width > 0) or (30 >= height > 0):
            return False, out_rec_list, out_pic_rect, classes_list
        else:
            first_man_number = randint(0, len(self.rec_objects_list) - 1)
            out_x1: int = self.rec_objects_list[first_man_number][0]
            out_y1: int = self.rec_objects_list[first_man_number][1]
            out_x2: int = self.rec_objects_list[first_man_number][2]
            out_y2: int = self.rec_objects_list[first_man_number][3]
            objects_in_cropped_images = [first_man_number]
            is_stop = True
            while is_stop:
                if out_x1 - width // 2 > 0:
                    out_x1 -= randint(0, width // 2)
                else:
                    out_x1 -= randint(0, out_x1)
                if out_y1 - height // 2 > 0:
                    out_y1 -= randint(0, height // 2)
                else:
                    out_y1 -= randint(0, out_y1)

                if out_x2 + width // 2 < self.img_width:
                    out_x2 += randint(0, width // 2)
                else:
                    if self.img_width - out_x2 > 0:
                        out_x2 += randint(0, self.img_width - out_x2)

                if out_y2 + height // 2 < self.img_height:
                    out_y2 += randint(0, height // 2)
                else:
                    if self.img_height - out_y2 > 0:
                        out_y2 += randint(0, self.img_height - out_y2)
                is_stop = False
                for i in range(len(self.rec_objects_list)):
                    if rectangles_intersection([out_x1, out_y1, out_x2, out_y2], 
                                                    [self.rec_objects_list[i][0],
                                                    self.rec_objects_list[i][1],
                                                    self.rec_objects_list[i][2],
                                                    self.rec_objects_list[i][3]]) \
                                                    and not (i in objects_in_cropped_images):
                        is_stop = True
                        if out_x1 > self.rec_objects_list[i][0]:
                            out_x1 = self.rec_objects_list[i][0]
                        if out_y1 > self.rec_objects_list[i][1]:
                            out_y1 = self.rec_objects_list[i][1]
                        if out_x2 < self.rec_objects_list[i][2]:
                            out_x2 = self.rec_objects_list[i][2]
                        if out_y2 < self.rec_objects_list[i][3]:
                            out_y2 = self.rec_objects_list[i][3]
                        objects_in_cropped_images.append(i)

            out_rec_list = []
            for number in objects_in_cropped_images:
                out_rec_list.append([self.rec_objects_list[number][0] - out_x1,
                                     self.rec_objects_list[number][1] - out_y1,
                                     self.rec_objects_list[number][2] - out_x1,
                                     self.rec_objects_list[number][3] - out_y1])
                classes_list.append(self.objects_classes[number])
            out_pic_rect = [out_x1, out_y1, out_x2, out_y2]
            if not (width == 0 or height == 0):
                new_width: int= out_x2 - out_x1
                new_height: int = out_y2 - out_y1
                multiplier_width: int = width / new_width
                multiplier_height: int = height / new_height
                img = self.get_image().crop((out_x1, out_y1, out_x2, out_y2))
                if multiplier_width < multiplier_height:
                    if not min_multiplier < multiplier_width < max_multiplier:
                        return False, out_rec_list, out_pic_rect, classes_list
                    else:
                        for line in out_rec_list:
                            x1 = line[0] * multiplier_width
                            y1 = line[1] * multiplier_width
                            x2 = line[2] * multiplier_width
                            y2 = line[3] * multiplier_width
                            new_line = [int(x1), int(y1), int(x2), int(y2)]
                            out_list_1.append(new_line)
                        new_image = img.resize((int(new_width * multiplier_width), int(new_height * multiplier_width)))
                else:
                    if not min_multiplier < multiplier_height < max_multiplier:
                        return False, out_rec_list, out_pic_rect, classes_list
                    else:
                        for line in out_rec_list:
                            x1 = line[0] * multiplier_height
                            y1 = line[1] * multiplier_height
                            x2 = line[2] * multiplier_height
                            y2 = line[3] * multiplier_height
                            new_line = [int(x1), int(y1), int(x2), int(y2)]
                            out_list_1.append(new_line)
                        new_image = img.resize(
                            (int(new_width * multiplier_height), int(new_height * multiplier_height)))
                return new_image, out_list_1, out_pic_rect, classes_list
            else:
                return self.get_image().crop((out_x1, out_y1, out_x2, out_y2)), out_rec_list, out_pic_rect, classes_list
