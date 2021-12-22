"""
 Author: Victor Gouromichos, Armin Nukic
"""
import numpy as np
import cv2
import time


def yolo_prediction(net, input_image):
    """
    The model net predicts on the picture input_image different objects

    Params:
        net: Holds the model of the AI
        input_image: Numpy array representation of the image

    Returns:
        layerOutputs which is an array with all the predictions and their corresponding score,
        which display the confidence of the prediction
    """

    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    blob = cv2.dnn.blobFromImage(input_image, 1 / 255.0, (416, 416),
                                 swapRB=True, crop=False)
    net.setInput(blob)
    start = time.time()
    layerOutputs = net.forward(ln)
    end = time.time()

    print("[INFO] YOLO took {:.6f} seconds".format(end - start))
    return layerOutputs


def get_prediction(image, conf):

    """
    Creates an image with the predictions and their classes and returns an array with the coordinates 
    of the bounding boxes and their corresponding classes

    Params:
        image: Numpay array represantion of the array 
        conf: A Config objection with all necessary configurations and paths

    Returns:
        boxes: Returns an array of arrays with four values, which represent the coordinates of the 
            predicted bounding boxes
        classIds: Returns an array of integers which describe, which object was detected at the
            corresponding indexes of boxes 

    """

    net = conf.nets
    LABELS = conf.labels
    COLORS = conf.colors

    # detected bounding boxes, with their confidence score and classID
    boxes = []
    confidences = []
    classIDs = []
    (H, W) = image.shape[:2]

    layerOutputs = yolo_prediction(net, image)

    # Node Output
    for output in layerOutputs:
        # Detection Output
        for detection in output:

            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            if confidence > conf.thresh_conf:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)

    #Non-Maxima Suppression
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, conf. thresh_conf,
                            conf.thresh_nms)

    # One detection found
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            color = [int(c) for c in COLORS[classIDs[i]]]
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
            print(boxes)
            print(classIDs)
            cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)

    cv2.imwrite('color_img.jpg', image)

    return boxes, classIDs
