import sys
from turtle import color
sys.path.append("..")
from flask import Blueprint, render_template, session,abort, request
from services.ColorFilter import ColorFilter
from services.Config import Config
import base64
import json
from cv2 import cv2
import numpy as np

config = Config()
color_filter = ColorFilter(config)

FilterColorController1 = Blueprint('FilterColorController1 ',__name__, url_prefix="/filtercolor")
@FilterColorController1.route("/", methods=('GET', 'POST'))
def filtercolor():
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
    color = json_data["color"]

    img = config.data_uri_to_cv2_img(image)
    cv2.imwrite(config.path_decoded_base64_image, img)
    img = cv2.imread(config.path_decoded_base64_image)

    result["image"] = base64.b64encode(color_filter.filter_color(img, color)).decode("utf-8")

    return result