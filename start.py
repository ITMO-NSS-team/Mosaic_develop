import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime
import sys

from MosaicController.MosaicController import MosaicController
from Constants.datatype_constants import YOLO, XVIEW, METU
from Constants.start_settings import REQUIRED_ARGS


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

    start = time.time()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    print(f"Current time: {dt_string}")
    parser = argparse.ArgumentParser(description="Mosaic data generator", formatter_class=RawTextHelpFormatter,
    epilog=('''
        Usage
        
        python3 start.py -t <TYPE> -s <start number> -e <end number> 
            -imputImagesFolder <imputImagesFolder> 
            -inputAnnotationsFolder <inputAnnotationsFolder>
            -outputImagesFolder <outputImagesFolder>
            -outputAnnotationsFolder <outputAnnotationsFolder>

        Generator now supports datasets in YOLO format.
        Also it supports METU and xView datasets. But using any other datasets in
        json-format annotations requires writing new datareader 
        because of differences in annotations' format and structures.
        Also now generator support only rectangle bounding boxes. WIP.

        '''))
    dataType_group = parser.add_argument_group()
    dataType_group.add_argument("-t", dest="TYPE", default="YOLO", type=str, \
        help="Type of input data, can be YOLO, METU, xVIEW datasets", required=REQUIRED_ARGS)

    mosaicNumber_group = parser.add_argument_group()
    mosaicNumber_group.add_argument("-s", dest="start_number", default="0", type=int, \
        help="Number of the first of mosaic that will be create", required=REQUIRED_ARGS)
    mosaicNumber_group.add_argument("-e", dest="end_number", default="10", type=int, \
        help="Number of the last of mosaic that will be create", required=REQUIRED_ARGS)

    inputPaths_group = parser.add_argument_group()
    inputPaths_group.add_argument("-imputImagesFolder", dest="imputImagesFolder", type=str, \
        help="Folder of images for mosaic", required=REQUIRED_ARGS)
    inputPaths_group.add_argument("-inputAnnotationsFolder", dest="inputAnnotationsFolder", type=str, \
        help="Folder/file of annotations for mosaic", required=REQUIRED_ARGS)

    outputPaths_group = parser.add_argument_group()
    outputPaths_group.add_argument("-outputImagesFolder", dest="outputImagesFolder", type=str, \
        help="Folder of images of mosaic", required=REQUIRED_ARGS)
    outputPaths_group.add_argument("-outputAnnotationsFolder", dest="outputAnnotationsFolder", type=str, \
        help="Folder of annotations of mosaic", required=REQUIRED_ARGS)

    args = parser.parse_args()

    if args.TYPE == "YOLO":
        data_type = YOLO
    elif args.TYPE == "METU":
        data_type = METU
    elif args.TYPE == "xVIEW":
        data_type = XVIEW
    else:
        print ("ERROR! Wrong dataset type was given!")
        sys.exit()
    
    Img_mosaic = MosaicController(args.imputImagesFolder, args.inputAnnotationsFolder, \
        args.outputImagesFolder, args.outputAnnotationsFolder, data_type)
    Img_mosaic.set_start_count(args.start_number)
    Img_mosaic.set_end_count(args.end_number)
    Img_mosaic.make_mosaic()
    end = time.time()
    print(f"Times taken: {end - start}")
