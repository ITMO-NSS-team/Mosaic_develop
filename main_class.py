import time
from ImageMosaic import ImageMosaic

start = time.time()
img_folder = "/home/balin/Downloads/archive(1)/aerial-cars-dataset/images/train"
txt_folder = "/home/balin/Downloads/archive(1)/aerial-cars-dataset/labels/train"
out_img_folder = "/home/balin/Downloads/archive(1)/aerial-cars-dataset/ready/"
out_txt_folder = "/home/balin/Downloads/archive(1)/aerial-cars-dataset/ready/"
Img_mosaic = ImageMosaic(img_folder, txt_folder, out_img_folder, out_txt_folder)
Img_mosaic.set_start_count(0)
Img_mosaic.set_end_count(500)
Img_mosaic.make_mosaic()
end = time.time()
print(end - start)
