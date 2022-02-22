"""
Author: Victor Gouromichos
"""
import sys
sys.path.append("..")
from flask import Blueprint, render_template, session,abort, request
from services.MaskCorrection import MaskCorrection
from services.PixelSegmentation import PixelSegmentation
from services.InpaintModel import InpaintModel
from services.Config import Config
import base64
import json
from cv2 import cv2
import numpy as np

config = Config()
pixel_segmentation = PixelSegmentation(config)
mask_correction = MaskCorrection(config)
inpaint_algo = InpaintModel(config)

InpaintController1 = Blueprint('InpaintController1 ',__name__, url_prefix="/inpaint")
@InpaintController1.route("/", methods=('GET', 'POST'))
def inpaint():
    """
    Callable by /inpaint through a GET or POST method
    Receives a picture and returns an inpainted image based on the specified Objects

    Params:
        image : Image, which will be inpainted
        object : List of object, which should be removed from the picture

    Returns:
        Inpainted picture
    """
    result = {}

    json_data = json.loads(request.data)
    image = json_data["image"]
    inpaint_list = json_data["object"]

    img = config.data_uri_to_cv2_img(image)
    cv2.imwrite(config.path_decoded_base64_image, img)

    img = cv2.imread(config.path_decoded_base64_image)
    resized_img = cv2.resize(img,(512, 512))
    img, black_img = pixel_segmentation.create_segmentation(resized_img.copy(), inpaint_list)

    print("len(img)")
    print(len(img))

    if(len(img) == 0):
        result["image"] = image
    else:
        output_mask_img = mask_correction.correct_mask(resized_img.copy() , black_img)
        inpainted_img = inpaint_algo.process_inpaint(output_mask_img)
        result["image"] = base64.b64encode(inpainted_img).decode("utf-8")
    
    return result