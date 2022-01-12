import sys
sys.path.append("..")
from flask import Blueprint, render_template, session,abort, request
from services.MaskCorrection import MaskCorrection
from services.PixellibSegmentation import PixellibSegmentation
from services.InpaintMaskRCNN import InpaintMaskRCNN
import base64
import json
from cv2 import cv2
import numpy as np

pixellib_segmentation = PixellibSegmentation()
mask_correction = MaskCorrection()
inpaint_algo = InpaintMaskRCNN()

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
    img = data_uri_to_cv2_img(image)
    data_name = './services/data/image.jpg'
    cv2.imwrite(data_name, img)

    img = cv2.imread('./services/data/menschlaufen.jpg')
    resized_img = cv2.resize(img,(512, 512))

    img, black_img = pixellib_segmentation.middle(resized_img.copy())
    output_mask_img = mask_correction.correct_mask(resized_img.copy() , black_img)
    inpainted_img = inpaint_algo.process_inpaint(output_mask_img)
    result["image"] = base64.b64encode(inpainted_img).decode("utf-8")
    return result

def data_uri_to_cv2_img(uri):
    encoded_data = uri
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print("data_uri_to_cv2_img fertig")
    return img