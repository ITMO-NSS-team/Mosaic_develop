from pickle import FALSE
from random import randint
#from tkinter import XView
from tqdm import tqdm
import logging
from MosaicContainer.MosaicContainer import MosaicContainer
from MosaicController.datasets_reading.xView import read_xView
from MosaicController.datasets_reading.yolov4  import read_yolov4
from MosaicController.datasets_reading.METU import read_METU
from Constants.datatype_constants import YOLO, XVIEW, METU
from Constants.mosaic_settings import MAX_MULTIPLIER, MIN_MULTIPLIER


class MosaicController:
    """
    Class-controller. Read images and annotations files into DataPair classes

    """
    pair_count: int
    input_image_folder: str
    input_text_folder: str
    output_image_folder: str
    output_txt_folder: str
    image_list: list
    txt_list: list
    img_ext = ".jpg"
    txt_ext = ".txt"
    pair_list = []

    min_object_multiplier: int
    max_object_multiplier: int

    start_number: int
    end_number: int
    max_images_in_mosaic = 5

    def __init__(self, input_img_folder: str, input_annotation_path: str,
                 output_img_folder: str, output_txt_folder: str, 
                 format: str, min_mult: float = MIN_MULTIPLIER,
                 max_mult: float = MAX_MULTIPLIER) -> None:
        """
        Constructor

        :param input_img_folder - folder to reading images
        :param input_txt_folder - folder to reading annotations
        :param output_img_folder - folder to writing images
        :param output_txt_folder - folder to writing annotations
        """
        logging.basicConfig(filename="mosaic_augment.log", level=logging.INFO)
        self.input_image_folder = input_img_folder
        self.min_object_multiplier = min_mult
        self.max_object_multiplier = max_mult
        self.start_number = 0
        self.end_number = 1
        self.output_image_folder = output_img_folder
        self.output_txt_folder = output_txt_folder
        self.input_text_folder = input_annotation_path
        if format == YOLO:
            _, self.pair_list = read_yolov4(input_img_folder, input_annotation_path)
        elif format == XVIEW:
            _, self.pair_list = read_xView(input_img_folder, input_annotation_path)
        elif format == METU:
            _, self.pair_list = read_METU(input_img_folder, input_annotation_path)
        self.pair_count = len(self.pair_list)

    def get_several_rand_pairs(self) -> list:
        """
        Create list of several random pairs

        :return list - pairs list
        
        """
        pic_number = randint(2, self.max_images_in_mosaic)
        rand_pairs_list = []
        for i in range(pic_number):
            stop = False
            while not stop:
                pair = randint(0, self.pair_count - 1)
                if self.pair_list[pair].object_number >= 1:
                    rand_pairs_list.append(pair)
                    stop = True

        logging.info(f"Chased {pic_number} images for mosaic. Images: {rand_pairs_list}")
        for i in range(pic_number):
            logging.info(f"People count on image number {i} - {rand_pairs_list[i]} = {self.pair_list[pair].object_number}")
        return rand_pairs_list

    def set_min_object_multiplier(self, new_multiplier) -> None:
        """
        Set min object multiplier
        """
        self.min_object_multiplier = new_multiplier

    def set_max_object_multiplier(self, new_multiplier) -> None:
        """
        Set max object multiplier
        """
        self.max_object_multiplier = new_multiplier

    def set_max_images_in_mosaic(self, new_max) -> None:
        """
        Set max images in mosaic
        """
        self.max_images_in_mosaic = new_max

    def set_start_count(self, count) -> None:
        """
        Set start count
        """
        self.start_number = count

    def set_end_count(self, count) -> None:
        """
        Set end count
        """
        self.end_number = count

    def print_params(self) -> None:
        """
        Print parameters of class
        """
        print(f"--------------------------------------------------")
        print("Parameters of class:")
        print(f"Minimum object multiplier = {self.min_object_multiplier}")
        print(f"Maximum object multiplier = {self.max_object_multiplier}")
        print(f"Open images folder: {self.input_image_folder}")
        print(f"Open annotations folder: {self.input_text_folder}")
        print(f"Save images folder: {self.output_image_folder}")
        print(f"Save annotations folder: {self.output_txt_folder}")
        print(f"Loaded pairs count: {self.pair_count}")
        print(f"Maximum images in mosaic {self.max_images_in_mosaic}")
        print(f"Start number {self.start_number}")
        print(f"End number {self.end_number}")
        print(f"--------------------------------------------------")
        logging.info(f"--------------------------------------------------")
        logging.info("Parameters of class:")
        logging.info(f"Minimum object multiplier = {self.min_object_multiplier}")
        logging.info(f"Maximum object multiplier = {self.max_object_multiplier}")
        logging.info(f"Open images folder: {self.input_image_folder}")
        logging.info(f"Open annotations folder: {self.input_text_folder}")
        logging.info(f"Save images folder: {self.output_image_folder}")
        logging.info(f"Save annotations folder: {self.output_txt_folder}")
        logging.info(f"Loaded pairs count: {self.pair_count}")
        logging.info(f"Maximum images in mosaic {self.max_images_in_mosaic}")
        logging.info(f"Start number {self.start_number}")
        logging.info(f"End number {self.end_number}")
        logging.info(f"--------------------------------------------------")

    def make_mosaic(self, ):
        """
        Make several mosaics from class data 
        """
        self.print_params()
        if self.end_number > self.start_number:
            if self.min_object_multiplier < self.max_object_multiplier:
                logging.info(f"Will be creating {self.end_number-self.start_number} mosaics")
                logging.info(f"From start number {self.start_number} to end number {self.end_number}")
                logging.info("Mosaic creation started...")
                print(f"Will be creating {self.end_number-self.start_number} mosaics")
                print(f"From start number {self.start_number} to end number {self.end_number}")
                print("Mosaic creation started...")
                for counter in tqdm(range(self.start_number, self.end_number), colour="green"):
                    have_to_do_mosaic = True
                    while(have_to_do_mosaic):
                        rand_pair_numbers = self.get_several_rand_pairs()
                        rand_pair_list = []
                        for i in range(len(rand_pair_numbers)):
                            rand_pair_list.append(self.pair_list[rand_pair_numbers[i]])
                        mosaic = MosaicContainer(rand_pair_list, self.output_image_folder, self.output_txt_folder, str(counter))
                        mosaic.min_object_multiplier = self.min_object_multiplier
                        mosaic.max_object_multiplier = self.max_object_multiplier
                        mosaic.img_ext = self.img_ext
                        mosaic.txt_ext = self.txt_ext
                        if mosaic.make_mosaic():
                            have_to_do_mosaic = False

                    logging.info(f"--------------------------------------------------")
            else:
                print("ERROR! Wrong multipliers!")
        else:
            print("ERROR! end < start")
