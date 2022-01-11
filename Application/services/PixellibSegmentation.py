import os
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
import numpy as np

class PixellibSegmentation():
    def __init__(self):
        self.img_size = 512
        self.model_config = './services/data/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt'
        self.model_weights = './services/data/frozen_inference_graph_coco.pb'
        self.colors = np.random.randint(125, 255, (90, 3))


    def Middle(self):
        img = cv2.imread('./services/data/menschlaufen.jpg')
        return self.CreateMaskAndPred(img)

    def CreateMaskAndPred(self, img):
        model = cv2.dnn.readNetFromTensorflow(self.model_weights, self.model_config)
        img = cv2.resize(img,(self.img_size, self.img_size))
        height, width, _ = img.shape
        black_image = np.zeros((height, width, 3), np.uint8)
        black_image[:] = (0, 0, 0)

        blob = cv2.dnn.blobFromImage(img, swapRB=True)
        model.setInput(blob)
        boxes, masks = model.forward(["detection_out_final", "detection_masks"])
        detection_count = boxes.shape[2]

        for i in range(detection_count):
            box = boxes[0, 0, i]
            class_id = box[1]
            score = box[2]
            if score < 0.5:
                continue
            print(class_id)
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
            contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            color = self.colors[int(class_id)]
            for cnt in contours:
                cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        cv2.imwrite('./services/data/output.png', np.hstack([img,black_image]))
        cv2.imwrite('./services/data/Overlay_image.png', ((0.6*black_image)+(0.4*img)).astype("uint8"))