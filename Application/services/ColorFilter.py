"""
Author: Victor Gouromichos
"""
import cv2
import numpy as np

class ColorFilter():
    """
    Object, which is responsible for the filtering of the colors
    """
    def __init__(self, config) -> None:
        """
        Initializes Colorfilter Object

        Params:
        Required Config Object with environment variables
        
        """
        self.config = config
        self.lower_blue = np.array([0, 0, 0])
        self.higher_blue = np.array([255, 90, 50])
        self.lower_red = np.array([0, 0, 0])
        self.higher_red = np.array([50, 90, 255])
        self.lower_green = np.array([0, 0, 0])
        self.higher_green = np.array([90, 255, 90])

    
    def filter_color(self, img, color):
        """
        Filters Colors, except the specified Color

        Params:
        img : Image, which will be filtered
        color : All Colors will be filtered, except the specified one
        
        Returns:
        The filtered Image
        """
        print("color")
        print(color)

        if(color == "blue"):
            mask = cv2.inRange(img,self.lower_blue, self.higher_blue) # Create a mask with range
        elif(color == "red"):
            mask = cv2.inRange(img,self.lower_red, self.higher_red) # Create a mask with range
        elif(color == "green"):
            mask = cv2.inRange(img,self.lower_green, self.higher_green) # Create a mask with range
        else:
            print("Wrong Specified Color")
            return img

        result = cv2.bitwise_and(img,img,mask = mask)
        
        cv2.imwrite('./services/data/colorfilter.png', result)

        return result
