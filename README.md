# Mosaic generator(augmenter)
### {WORK IN PROGRESS}

++This project is lossles mosaic generator. All craftsdwarfship is of highest quality.++
It's provide one single function - generate mosaic data from your dataset.

### Purpose

There is a lot of troubles with creating dataset good enough for training of neural networks sutable for your purpose. One of the hardest - you have too little datapairs in your dataset. Also it can be too few objects on the images or too much free space around objects. Such data pairs can't provide any good information for training. In this case you can use the mosaic augmenter. 

Most mosaic augmenters combine several parts of images from the dataset to create a new piece of data. But most of them cut objects on the main images, or on images for inserting. This can be dangerous for precision of training model.

So I create this augmenter to create better augmented datasets -  lossles mosaic generator. Lossles mosaic generatot works as follows: generator places numerous points on the main image with random coordinates and looks for points outside any of images objects. After it generator creates a random rectangle area around each of such points and looks for intersections with any object (Picture 1, left image, blue rectangle). If an intersection is found, GWL resizes the area to avoid intersection for each object (Picture 1, left image, red rectangle). GWL gets one rectangle with the biggest area from the list. Then GWL seeks for space of similar size with one or more objects in another picture and pastes it in found free space. Searching for areas with objects works similar to searching for empty areas presented in (Picture 1, right image, blue rectangle). But instead of placing points, system choose random object and creates a rectangle around it. Also, rectangles are resizing to the biggest size to avoid cutting off any parts of objects as presented in (Picture 1, right image, red rectangle). 

![Example](https://i.imgur.com/SHcWvi9.png)
Picture 1: The example of a searching process for a) empty area, a blue rectangle is a random area that includes objects, the red rectangle is a resized empty area; b) area with objects, blue rectangle is an are with area's borders intersect with bounding boxes of objects, blue rectangle is an area without any intersections between its borders and any of bounding boxes.

At the end of readme shown examples of random placing on several datasets, 


Now this generator supports datasets in bot variations pf YOLO format:

      object-class x y width height
      object-class x1 y1 x2 y2
  
In plans - add support for COCO formatted datasets.

Above it, generator supports two specific datasets: 

      xView (https://challenge.xviewdataset.org/login)
      METU-ALET (https://github.com/metu-kovan/METU-ALET).
  
### Usage
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
        
### Examples

![Example](https://i.imgur.com/4bS60Dv.png)
![Example](https://i.imgur.com/2Bbab22.png)
![Example](https://i.imgur.com/CgKTtb8.png)

![Example](https://i.imgur.com/mhKn6zd.png)
![Example](https://i.imgur.com/QyP9meU.png)
![Example](https://i.imgur.com/2ELSxcE.png)
