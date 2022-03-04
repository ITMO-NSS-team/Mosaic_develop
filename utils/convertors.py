def from_yolo_to_rec(x: int, y: int, width: int, height: int, image_width: int, image_height: int) -> list:
        """
        This method turns annotations in YOLO format into rectangle coordinates
        """
        box_w = int(width * image_width)
        box_h = int(height * image_height)
        x_mid = int(x * image_width + 1)
        y_mid = int(y * image_height + 1)
        x_min = int(x_mid - box_w / 2) + 1
        x_max = int(x_mid + box_w / 2) - 1
        y_min = int(y_mid - box_h / 2) + 1
        y_max = int(y_mid + box_h / 2) - 1
        return [x_min, y_min, x_max, y_max]

def from_yolo_to_rec(box: list, image_width: int, image_height: int) -> list:
        """
        This method turns annotations in YOLO format into rectangle coordinates
        """
        box_w = int(box[2] * image_width)
        box_h = int(box[3] * image_height)
        x_mid = int(box[0] * image_width + 1)
        y_mid = int(box[1] * image_height + 1)
        x_min = int(x_mid - box_w / 2) + 1
        x_max = int(x_mid + box_w / 2) - 1
        y_min = int(y_mid - box_h / 2) + 1
        y_max = int(y_mid + box_h / 2) - 1
        return [x_min, y_min, x_max, y_max]

def from_rec_to_yolo(x1: int, y1: int, x2: int, y2: int, image_width: int, image_height: int) -> list:
        """
        Turn rectangular coordinates in YOLO format

        :return list - YOLO coordinates
        """
        dw = 1. / image_width
        dh = 1. / image_height
        x = (x1 + x2) / 2.0
        y = (y1 + y2) / 2.0
        w = x2 - x1
        h = y2 - y1
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return [x, y, w, h]

def from_rec_to_yolo(box, image_width: int, image_height: int) -> list:
        """
        Turn rectangular coordinates in YOLO format

        :return list - YOLO coordinates
        """
        dw = 1. / image_width
        dh = 1. / image_height
        x = (box[0] + box[2]) / 2.0
        y = (box[1] + box[3]) / 2.0
        w = box[2] - box[0]
        h = box[3] - box[1]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return [x, y, w, h]