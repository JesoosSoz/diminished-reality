import sys
sys.path.append("..")
from flask import Blueprint, render_template, session,abort, request
from services.MaskCorrection import MaskCorrection
from services.PixellibSegmentation import PixellibSegmentation
from services.InpaintMaskRCNN import InpaintMaskRCNN
from services.Config import Config
import base64
import json
from cv2 import cv2
import numpy as np

config = Config()
pixellib_segmentation = PixellibSegmentation(config)
mask_correction = MaskCorrection(config)
inpaint_algo = InpaintMaskRCNN(config)

InpaintController1 = Blueprint('InpaintController1 ',__name__, url_prefix="/order")
@InpaintController1.route("/", methods=('GET', 'POST'))
def picture():
    """
    Callable by /picture through a GET method
    Retrieves the latest picture with the predictions made by the AI

    Params:

    Returns:
        The latest taken picture with predictions encoeded in base64
    """
    result = {}

    json_data = json.loads(request.data)
    image = json_data["image"]
    inpaint_list = json_data["object"]

    img = config.data_uri_to_cv2_img(image)
    cv2.imwrite(config.path_decoded_base64_image, img)

    img = cv2.imread(config.path_decoded_base64_image)
    resized_img = cv2.resize(img,(512, 512))
    img, black_img = pixellib_segmentation.middle(resized_img.copy(), inpaint_list)

    print("len(img)")
    print(len(img))

    if(len(img) == 0):
        result["image"] = image
    else:
        output_mask_img = mask_correction.correct_mask(resized_img.copy() , black_img)
        inpainted_img = inpaint_algo.process_inpaint(output_mask_img)
        result["image"] = base64.b64encode(inpainted_img).decode("utf-8")
    
    return result