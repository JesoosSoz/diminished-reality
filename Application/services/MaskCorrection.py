"""
Author: Victor Gouromichos
"""
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from cv2 import cv2

class MaskCorrection():
    def __init__(self, config):
        self.config = config
        self.image_inpaint = 9

    def correct_mask(self, img, black_image):

        onebite_masc = cv2.cvtColor(black_image, cv2.COLOR_BGR2GRAY)
        img_pre_output = img.copy()
        img_output = img.copy()

        j = 0
        for row in img_pre_output:
            i = 0
            for element in row:
                if (onebite_masc[j, i] != 0):
                    row[i] = [255, 255, 255]
                i = i + 1
            # print(row)
            j = j + 1

        j = 0
        for row in img_pre_output:
            i = 0
            for element in row:
                if np.array_equal(element, [255, 255, 255]):
                        img_output = cv2.circle(img_output, (i, j), self.image_inpaint, (255, 255, 255), 0)
                i = i + 1
            j = j + 1
            
        mask_output = img_output.copy()

        j = 0
        for row in mask_output:
            i = 0
            for element in row:
                if not np.array_equal(element, [255, 255, 255]):
                    row[i] = [0, 0, 0]
                i = i + 1
            # print(row)
            j = j + 1

        final_onebite_masc = cv2.cvtColor(mask_output, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(self.config.path_to_mask, final_onebite_masc)
        dst = cv2.inpaint(img,final_onebite_masc,3,cv2.INPAINT_TELEA)
        output_mask_img = cv2.add(img,mask_output)
        
        return output_mask_img