# Mosaic generator
### {WORK IN PROGRESS}

This project is lossles mosaic generator.  


Now this generator supports datasets in bot variations pf YOLO format:

      object-class x y width height
      object-class x1 y1 x2 y2
  
In plans - add support for COCO formatted datasets.

Above it, generator supports two specific datasets: xView (https://challenge.xviewdataset.org/login) and METU-ALET (https://github.com/metu-kovan/METU-ALET).
  



### Examples
***

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
