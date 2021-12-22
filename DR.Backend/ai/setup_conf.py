"""
 Author: Victor Gouromichos, Armin Nukic
"""
import numpy as np
import cv2
import base64

class config():
    """
    Saves often used variables in a config object and initially load the models.
    """
    def __init__(self):
        """
        Initialize the most used and static variables and preload the models.
        """
        self.thresh_conf = 0.4
        self.thresh_nms = 0.1
        self.coco_names_path = "./configs/coco.names"
        self.weights_path = "./configs/yolov3.weights"
        self.cfg_path = "./configs/yolov3.cfg"
        self.nets = self.load_model()
        self.get_labels_and_colors()

    def load_model(self):
        """
        Loads the model for our predictions

        Params:
        
        Returns:
        An object of the model
        """
        print("Loading Yolo")
        net = cv2.dnn.readNetFromDarknet(self.cfg_path, self.weights_path)
        return net

    def get_labels_and_colors(self):
        """
        Loads the names of the objects that can be identified and a random set of colors
        """
        self.labels = open(self.coco_names_path).read().strip().split("\n")
        np.random.seed(42)
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3),dtype="uint8")

def data_uri_to_cv2_img(uri):
    """
    Decodes the base64 image for cv2 library to read
    
    Params:
    uri: A String

    Returns:
    An image that gets created from the uri
    """
    encoded_data = uri
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img