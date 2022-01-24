"""
 Author: Victor Gouromichos, Armin Nukic
"""

import numpy as np
import argparse
import time
import cv2
import os
from time import sleep

from ai.yolo import yolo_prediction, get_predection

confthres=0.4
nmsthres=0.1

def get_direction(boxes, classIDs, search, shape):
    """
    Get the side on which the object stands in the picture and an offset percentage,
    how much it is away from the middle of the picture taken if the searched for object is found
    
    Params:
    boxes: Array of Picture coordinates
    classIDs: Array of the ID's of found objects
    search:A String
    shape:Data of the picture size in an Array

    Returns:
    Direction to which the robot should turn (left,right) and the percentage offset of the object from the middle (for example 0.2 or 0.47)
    """

    if(search in classIDs):
        Index = classIDs.index(search)
        found_boxes = boxes[Index]
        x = found_boxes[0]
        width = found_boxes[2]
        calc_x = (x + width / 2)
        per = calc_x / shape[1]

        if(per < 0.5):
            direc = "left"
        else:
            direc = "right"
        per = abs(per - 0.5)

        return direc, per
    else:
        return "nichts", 0


def get_prediction(search, image, conf):
    """
    Gets the prediction of items found in the picture and returns direction and percentage
    
    Params:
    search: A String
    image: A image
    conf: The config object

    Returns:
    Direction and percentage to which the robot should turn to and how far
    """

    boxes, classIDs = get_predection(image, conf)

    search_index = conf.labels.index(search)
    direction, percentage = get_direction(boxes, classIDs, search_index, image.shape)

    return direction, percentage