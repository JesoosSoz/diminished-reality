"""
 Author: Victor Gouromichos, Armin Nukic
"""
from flask import Flask, request, jsonify
import base64
from ai.predict import get_prediction
import cv2
import numpy as np
from ai.setup_conf import data_uri_to_cv2_img, config

app = Flask(__name__)

conf = config()

@app.route("/picture", methods=["GET"])
def picture():
    """
    Callable by /picture through a GET method
    Retrieves the latest picture with the predictions made by the AI

    Params:

    Returns:
        The latest taken picture with predictions encoeded in base64
    """

    with open("./color_img.jpg", "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    return im_b64

@app.route("/prediction", methods=["POST"])
def prediction():
    """
    Callable by /prediction through a POST method
    Receives a picture and predicts where certain objects are.
    
    Params:
        search: a String, which object the AI should search
        image: a base64 decoded Image as String

    Returns:
        A String with the direction of the searched object 
        and the distance between the object and the center of the picture
    """
    data = request.json
    search = data["search"]
    img = data_uri_to_cv2_img(data["image"])
    direction, percentage = get_prediction(search, img, conf)
    print(direction)
    print(percentage)
    print(str([direction, percentage]))
    return str([direction, percentage]), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0')
