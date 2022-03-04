import time
from MosaicController.MosaicController import MosaicController
from Constants.datatype_constants import YOLO, XVIEW, METU

start = time.time()

images = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4"
json_file = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4.json" 

img_folder = "/media/nikita/HDD/datasets/xView/train_images/train_images"
txt_folder = "/media/nikita/HDD/datasets/xView/train_labels/xView_train.geojson"
out_img_folder = "/media/nikita/HDD/test/img/"
out_txt_folder = "/media/nikita/HDD/test/txt/"
Img_mosaic = MosaicController(images, json_file, out_img_folder, out_txt_folder, METU)
Img_mosaic.set_start_count(0)
Img_mosaic.set_end_count(50)
Img_mosaic.make_mosaic()
end = time.time()
print(end - start)
