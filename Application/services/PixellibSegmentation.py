from copy import deepcopy
from operator import truediv
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from cv2 import cv2

class PixellibSegmentation():
    def __init__(self, config):
        self.config = config
        self.img_size = 512
        self.colors = np.random.randint(125, 255, (90, 3))


    def create_segmentation(self, resized_img, inpaint_list):
        """A dummy docstring."""
        boxes, masks = self.detection(resized_img)
        img, black_img, count = self.draw_segmentation(boxes, masks, resized_img, inpaint_list)
        print("count")
        print(count)
        if(count == 0):
            return [],[]
        else:
            return img, black_img

    def detection(self, img):
        """A dummy docstring."""
        model = cv2.dnn.readNetFromTensorflow(self.config.path_to_coco_weights, self.config.path_to_coco_config)
        blob = cv2.dnn.blobFromImage(img, swapRB=True)
        model.setInput(blob)
        boxes, masks = model.forward(["detection_out_final", "detection_masks"])
        return boxes, masks

    def draw_segmentation(self, boxes, masks, img, inpaint_list):
        height, width, _ = img.shape
        black_image = np.zeros((height, width, 3), np.uint8)
        black_image[:] = (0, 0, 0)
        count = 0

        detection_count = boxes.shape[2]

        for i in range(detection_count):
            box = boxes[0, 0, i]
            class_id = box[1]
            score = box[2]
            
            if score < 0.5  or self.object_not_in_inpaintlist(inpaint_list, class_id):
                continue
            print(class_id)
            count = count + 1
            x = int(box[3] * width)
            y = int(box[4] * height)
            x2 = int(box[5] * width)
            y2 = int(box[6] * height)
            roi = black_image[y: y2, x: x2]
            roi_height, roi_width, _ = roi.shape
            mask = masks[i, int(class_id)]
            mask = cv2.resize(mask, (roi_width, roi_height))
            _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)
            cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 3)
            contours, _ = cv2.findContours(np.array(mask, np.uint8), 
                            cv2.RETR_EXTERNAL, 
                            cv2.CHAIN_APPROX_SIMPLE)
            color = self.colors[int(class_id)]
            for cnt in contours:
                cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        cv2.imwrite('./services/data/output.png', np.hstack([img,black_image]))
        cv2.imwrite('./services/data/Overlay_image.png', ((0.6*black_image)+(0.4*img)).astype("uint8"))

        return img, black_image, count
    
    def object_not_in_inpaintlist(self, inpaint_list, class_id):
        print("class_id")
        print(class_id)
        print(inpaint_list)


        inpaint_object = self.config.labels[int(class_id)]

        if(inpaint_object in inpaint_list):
            print("False")
            return False
        else:
            print("True")
            return True
            

    