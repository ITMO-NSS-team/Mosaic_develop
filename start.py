import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime
import sys

from MosaicController.MosaicController import MosaicController
from Constants.datatype_constants import YOLO, XVIEW, METU


if __name__ == "__main__":
    # --help - help and manual
    # -t <TYPE> - type of input data, can be YOLO, METU, xVIEW datasets -
    # -s <start number> <end number> - number of the first of mosaic that will be create
    # -e <start number> <end number> - number of the last of mosaic that will be create
    # Count of mosaic = <end number> - <start number> 
    # -inputImagesFolder <input images folder> - folder of images for mosaic
    # -inputAnnotationsFolder <input annotations folder> - folder/file of annotations for mosaic

    # -outputImagesFolder <output images folder> - folder of images of mosaic
    # -outputAnnotationsFolder <output annotations folder> - folder of annotations of mosaic

    # -m - ручной режим работы -
    # -v - вывод списка дисков и регистраций -
    # Константы для форматированного вывода и файла регистрации
    start = time.time()
    required_args = True
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"Current time: {dt_string}")
    parser = argparse.ArgumentParser(description="Mosaic data generator", formatter_class=RawTextHelpFormatter,
    epilog=('''
    Test now
    '''))
    dataType_group = parser.add_argument_group()
    dataType_group.add_argument("-t", dest="TYPE", default="YOLO", type=str, \
        help=" Type of input data, can be YOLO, METU, xVIEW datasets", required=required_args)

    mosaicNumber_group = parser.add_argument_group()
    mosaicNumber_group.add_argument("-s", dest="start_number", default="0", type=int, \
        help=" Number of the first of mosaic that will be create", required=required_args)
    mosaicNumber_group.add_argument("-e", dest="end_number", default="10", type=int, \
        help=" Number of the last of mosaic that will be create", required=required_args)

    inputPaths_group = parser.add_argument_group()
    inputPaths_group.add_argument("-imputImagesFolder", dest="imputImagesFolder", type=str, \
        help=" Folder of images for mosaic", required=required_args)
    inputPaths_group.add_argument("-inputAnnotationsFolder", dest="inputAnnotationsFolder", type=str, \
        help=" Folder/file of annotations for mosaic", required=required_args)

    outputPaths_group = parser.add_argument_group()
    outputPaths_group.add_argument("-outputImagesFolder", dest="outputImagesFolder", type=str, \
        help=" Folder of images of mosaic", required=required_args)
    outputPaths_group.add_argument("-outputAnnotationsFolder", dest="outputAnnotationsFolder", type=str, \
        help=" Folder of annotations of mosaic", required=required_args)

    args = parser.parse_args()

    if args.TYPE == "YOLO":
        print ("It works! YOLO")
        data_type = YOLO
    elif args.TYPE == "METU":
        print ("It works! METU")
        data_type = METU
    elif args.TYPE == "xVIEW":
        print ("It works! xVIEW")
        data_type = XVIEW
    else:
        print ("ERROR! Wrong dataset type was given!")
        sys.exit()

    print (args.start_number)
    print (args.end_number)

    images = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4"
    json_file = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4.json" 



    img_folder = '/home/balin/Downloads/archive(1)/aerial-cars-dataset/images/train/'
    txt_folder = '/home/balin/Downloads/archive(1)/aerial-cars-dataset/labels/train' 
    out_img_folder = "/mnt/HDD/mosaics/img"
    out_txt_folder = "/mnt/HDD/mosaics/txt"
    """
    Img_mosaic = MosaicController(img_folder, txt_folder, \
        out_img_folder, out_txt_folder, YOLO)
    Img_mosaic.set_start_count(0)
    Img_mosaic.set_end_count(2000)
    Img_mosaic.make_mosaic()
    """
    
    """
    
    /usr/bin/python3 /home/balin/Desktop/Mosaic_develop/start.py 
    -t YOLO -s 0 -e 100  -imputImagesFolder 
    '/home/balin/Downloads/archive(1)/aerial-cars-dataset/images/train/' 
    -inputAnnotationsFolder 
    '/home/balin/Downloads/archive(1)/aerial-cars-dataset/labels/train' 
    -outputImagesFolder 
    /mnt/HDD/mosaics/img -outputAnnotationsFolder /mnt/HDD/mosaics/txt
    """
    Img_mosaic = MosaicController(args.imputImagesFolder, args.inputAnnotationsFolder, \
        args.outputImagesFolder, args.outputAnnotationsFolder, data_type)
    Img_mosaic.set_start_count(args.start_number)
    Img_mosaic.set_end_count(args.end_number)
    Img_mosaic.make_mosaic()
    end = time.time()
    print(end - start)
