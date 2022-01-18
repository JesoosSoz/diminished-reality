import cv2
import numpy as np
import base64

class Config():
    def __init__(self):
        self.coco_names_path = "./services/data/coco.names"
        self.labels = open(self.coco_names_path).read().strip().split("\n")
        self.path_decoded_base64_image = './services/data/image.jpg'
        self.path_to_coco_weights = './services/data/frozen_inference_graph_coco.pb'
        self.path_to_coco_config = './services/data/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt'
        self.path_to_inpaintprediction = './services/data/prediction.png'
        self.path_to_masc = "./services/data/mask.png"
        self.path_to_inpaint_weights = "./services/data/weights.26-1.07.h5"
        self.path_to_mask = "./services/data/mask.png"


    def data_uri_to_cv2_img(self, uri):
        encoded_data = uri
        nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        print("data_uri_to_cv2_img fertig")
        return img

