class Config():
    def __init__(self):
        self.coco_names_path = "./services/data/coco.names"
        self.labels = open(self.coco_names_path).read().strip().split("\n")
        self.path_decoded_base64_image = './services/data/image.jpg'
        self.path_to_coco_weights = './services/data/frozen_inference_graph_coco.pb'
        self.path_to_coco_config = './services/data/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt'

