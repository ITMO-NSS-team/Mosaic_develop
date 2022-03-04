import time
from MosaicController.MosaicController import MosaicController
from Constants.datatype_constants import YOLO, XVIEW, METU

start = time.time()

images = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4"
json_file = "/media/nikita/HDD/datasets/METU-ALET/ALET/trainv4.json" 

img_folder = "/media/nikita/HDD/datasets/xView/train_images/train_images"
txt_folder = "/media/nikita/HDD/datasets/xView/train_labels/xView_train.geojson"
out_img_folder = "/media/nikita/HDD/test/xView/img/"
out_txt_folder = "/media/nikita/HDD/test/xView/txt/"
Img_mosaic = MosaicController(img_folder, txt_folder, out_img_folder, out_txt_folder, XVIEW)
Img_mosaic.set_start_count(0)
Img_mosaic.set_end_count(2000)
Img_mosaic.make_mosaic()
end = time.time()
print(end - start)
